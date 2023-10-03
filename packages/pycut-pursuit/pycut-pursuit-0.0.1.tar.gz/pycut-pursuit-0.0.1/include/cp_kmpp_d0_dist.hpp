/*=============================================================================
 * Derived class for cut-pursuit algorithm with d0 (weighted contour length) 
 * penalization, with a loss akin to a distance:
 *
 * minimize functional over a graph G = (V, E)
 *
 *        F(x) = sum_v loss(y_v, x_v) + ||x||_d0
 *
 * where for each vertex, y_v and x_v are D-dimensional vectors, the loss is
 * either the sum of square differences or smoothed Kullback-Leibler divergence
 * (equivalent to cross-entropy in this formulation); see the 'loss' attribute,
 *   and ||x||_d0 = sum_{uv in E : xu != xv} w_d0_uv ,
 *
 * using greedy cut-pursuit approach with splitting initialized with k-means++.
 *
 * Parallel implementation with OpenMP API.
 *
 * L. Landrieu and G. Obozinski, Cut Pursuit: fast algorithms to learn
 * piecewise constant functions on general weighted graphs, SIAM Journal on
 * Imaging Science, 10(4):1724-1766, 2017
 *
 * L. Landrieu et al., A structured regularization framework for spatially
 * smoothing semantic labelings of 3D point clouds, ISPRS Journal of
 * Photogrammetry and Remote Sensing, 132:102-118, 2017
 *
 * Hugo Raguet 2019
 *===========================================================================*/
#pragma once
#include <cmath>
#include "cut_pursuit_d0.hpp"

/* real_t is the real numeric type, used for the base field and for the
 * objective functional computation;
 * index_t must be able to represent the number of vertices and of (undirected)
 * edges in the main graph;
 * comp_t must be able to represent the number of constant connected components
 * in the reduced graph */
template <typename real_t, typename index_t, typename comp_t>
class Cp_d0_dist : public Cp_d0<real_t, index_t, comp_t>
{
public:
    /**  constructor, destructor  **/

    /* only creates BK graph structure and assign Y, D */
    Cp_d0_dist(index_t V, index_t E, const index_t* first_edge,
        const index_t* adj_vertices, const real_t* Y, size_t D = 1);

    /* the destructor does not free pointers which are supposed to be provided 
     * by the user (forward-star graph structure given at construction, 
     * monitoring arrays, observation arrays); IT DOES FREE THE REST 
     * (components assignment and reduced problem elements, etc.), but this can
     * be prevented by getting the corresponding pointer member and setting it
     * to null beforehand */
	~Cp_d0_dist();

    /**  methods for manipulating parameters  **/

    /* specific loss */
    static real_t quadratic_loss() { return 1.0; }

    /* Y is changed only if the corresponding argument is not null */
    void set_loss(real_t loss, const real_t* Y = nullptr,
        const real_t* vert_weights = nullptr,
        const real_t* coor_weights = nullptr);

    /* overload for changing only loss weights */
    void set_loss(const real_t* vert_weights = nullptr,
        const real_t* coor_weights = nullptr)
        { set_loss(loss, nullptr, vert_weights, coor_weights); }

    void set_kmpp_param(int kmpp_init_num = 3, int kmpp_iter_num = 3);

    void set_min_comp_weight(real_t min_comp_weight = 1.0);

private:
    /**  separable loss term: weighted square l2 or smoothed KL **/
    const real_t* Y; // observations, D-by-V array, column major format

    /* 1 for quadratic (function quadratic_loss())
     *      f(x) = 1/2 ||y - x||_{l2,W}^2 ,
     * where W is a diagonal metric (separable product along ℝ^V and ℝ^D),
     * that is ||y - x||_{l2,W}^2 = sum_{v in V} w_v ||x_v - y_v||_{l2,M}^2
     *                            = sum_{v in V} w_v sum_d m_d (x_vd - y_vd)^2.
     *
     * 0 < loss < 1 for (smoothed, weighted) Kullback-Leibler divergence
     * (cross-entropy) on the probability simplex
     *     f(x) = sum_v w_v KLs_m(x_v, y_v),
     * with KLs(y_v, x_v) = KL_m(s u + (1 - s) y_v ,  s u + (1 - s) x_v), where
     *     KL is the regular Kullback-Leibler divergence,
     *     u is the uniform discrete distribution over {1,...,D}, and
     *     s = loss is the smoothing parameter
     *     m is a diagonal metric weighting the coordinates;
     * it yields
     *     KLs_m(y_v, x_v) = - H_m(s u + (1 - s) y_v)
     *         - sum_d m_d (s/D + (1 - s) y_{v,d}) log(s/D + (1 - s) x_{v,d}) ,
     * where H_m is the (weighted) entropy, that is H_m(s u + (1 - s) y_v)
     *       = - sum_d m_d (s/D + (1 - s) y_{v,d}) log(s/D + (1 - s) y_{v,d}) ;
     * note that the choosen order of the arguments in the Kullback--Leibler
     * does not favor the entropy of x (H_m(s u + (1 - s) y_v) is a constant),
     * hence this loss is actually equivalent to cross-entropy;
     *
     * the weights w_v are set in vert_weights and m_d are set in coor_weights;
     * set corresponding pointer to null for no weight */
    real_t loss;
    const real_t *vert_weights, *coor_weights;

    /* minimum weight allowed for a component */
    real_t min_comp_weight;

    /* compute the functional f at a single vertex */
    /* NOTA: not actually a metric, in spite of its name */
    real_t distance(const real_t* Xv, const real_t* Yv);
    real_t fv(index_t v, const real_t* Xv) override;
    /* override for storing values (used for iterate evolution) */
    real_t compute_f() override;
    real_t fXY; // dist(X, Y), reinitialized when freeing rX
    real_t fYY; // dist(Y, Y), reinitialized when modifying the loss

    /**  reduced problem  **/
    real_t* comp_weights;

    /* allocate and compute reduced values;
     * do nothing if the array of reduced values is not null */
    void solve_reduced_problem() override;

    /**  greedy splitting  **/

    int kmpp_init_num; // number of random k-means initializations
    int kmpp_iter_num; // number of k-means iterations

    real_t component_average(comp_t rv, real_t* avgXv);

    /* rough estimate of the number of operations for initializing and
     * updating the split values */
    uintmax_t split_values_complexity() override;
    void init_split_values(comp_t rv, real_t* altX) override; // k-means ++
    void update_split_values(comp_t rv, real_t* altX) override; // average
    bool is_split_value(real_t altX) override; // flag with infinity

    /**  merging components **/
    using typename Cp_d0<real_t, index_t, comp_t>::Merge_info;

    /* update information of the given merge candidate in the list;
     * merge information must be created with new and destroyed with delete;
     * negative gain values might still get accepted; for inacceptable gain,
     * do not create (or destroy if it exists) the merge information and flag
     * it with a null pointer
     TODO: rewrite */
    void update_merge_info(Merge_info&) override;

    /* rough estimate of the number of operations for updating all candidates;
     * useful for estimating the number of parallel threads
     TODO: change name */
    size_t update_merge_complexity() override;

    /* accept the merge candidate and return the component root of the
     * resulting merge chain
     TODO: rewrite */
    comp_t accept_merge(const Merge_info&) override;

    index_t merge() override; // override for freeing comp_weights

    /**  monitoring evolution  **/

   /* relative relative iterate evolution in l2 norm; parameters not used */
    real_t compute_evolution(bool compute_dif) override;

    /**  type resolution for base template class members  **/
    using Cp_d0<real_t, index_t, comp_t>::K;
    using Cp_d0<real_t, index_t, comp_t>::split_iter_num;
    using Cp<real_t, index_t, comp_t>::D;
    using Cp<real_t, index_t, comp_t>::rX;
    using Cp<real_t, index_t, comp_t>::last_rX;
    using Cp<real_t, index_t, comp_t>::saturated_comp;
    using Cp<real_t, index_t, comp_t>::saturated_vert;
    using Cp<real_t, index_t, comp_t>::last_comp_assign;
    using Cp<real_t, index_t, comp_t>::eps;
    using Cp<real_t, index_t, comp_t>::V;
    using Cp<real_t, index_t, comp_t>::E;
    using Cp<real_t, index_t, comp_t>::first_edge;
    using Cp<real_t, index_t, comp_t>::adj_vertices; 
    using Cp<real_t, index_t, comp_t>::edge_weights;
    using Cp<real_t, index_t, comp_t>::homo_edge_weight;
    using Cp<real_t, index_t, comp_t>::rV;
    using Cp<real_t, index_t, comp_t>::rE;
    using Cp<real_t, index_t, comp_t>::comp_assign;
    using Cp<real_t, index_t, comp_t>::label_assign;
    using Cp<real_t, index_t, comp_t>::comp_list;
    using Cp<real_t, index_t, comp_t>::first_vertex;
    using Cp<real_t, index_t, comp_t>::index_in_comp;
    using Cp<real_t, index_t, comp_t>::reduced_edge_weights;
    using Cp<real_t, index_t, comp_t>::is_saturated;
    using Cp<real_t, index_t, comp_t>::verbose;
    using Cp<real_t, index_t, comp_t>::malloc_check;
    using Cp<real_t, index_t, comp_t>::real_inf;
};

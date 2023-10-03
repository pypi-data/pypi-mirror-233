/*=============================================================================
 * Derived class for cut-pursuit algorithm with d0 (weighted contour length) 
 * penalization, with a separable loss term over a given space:
 *
 * minimize functional over a graph G = (V, E)
 *
 *        F(x) = f(x) + ||x||_d0
 *        
 * where for each vertex, x_v belongs in a possibly multidimensional space Ω,
 *       f(x) = sum_{v in V} f_v(x_v) is separable along V with f_v : Ω → ℝ
 *   and ||x||_d0 = sum_{uv in E : xu != xv} w_d0_uv ,
 *
 * using greedy cut-pursuit approach.
 *
 * Parallel implementation with OpenMP API.
 *
 * References: 
 *
 * L. Landrieu and G. Obozinski, Cut Pursuit: fast algorithms to learn
 * piecewise constant functions on general weighted graphs, SIAM Journal on
 * Imaging Science, 10(4):1724-1766, 2017
 *
 * L. Landrieu et al., A structured regularization framework for spatially
 * smoothing semantic labelings of 3D point clouds, ISPRS Journal of
 * Photogrammetry and Remote Sensing, 132:102-118, 2017
 *
 * Hugo Raguet 2019, 2020
 *===========================================================================*/
#pragma once
#include "cut_pursuit.hpp"

/* real_t is the real numeric type, used for objective functional computation;
 * index_t must be able to represent the number of vertices and of (undirected)
 * edges in the main graph;
 * comp_t must be able to represent the number of constant connected components
 * in the reduced graph;
 * value_t is the type associated to the space to which the values belong, it
 * is usually real_t, and if multidimensional, this must be specified in the
 * parameter D (e.g. for R^3, specify value_t = real_t and D = 3) */
template <typename real_t, typename index_t, typename comp_t,
    typename value_t = real_t>
class Cp_d0 : public Cp<real_t, index_t, comp_t, value_t>
{
public:
    Cp_d0(index_t V, index_t E, const index_t* first_edge, 
        const index_t* adj_vertices, size_t D = 1);

    /* the destructor does not free pointers which are supposed to be provided 
     * by the user (forward-star graph structure given at construction, 
     * edge weights, etc.); IT DOES FREE THE REST (components assignment 
     * and reduced problem elements, etc.), but this can be prevented by
     * getting the corresponding pointer member and setting it to null
     * beforehand */

    void set_split_param(comp_t K = 2, int split_iter_num = 2,
        real_t split_damp_ratio = 1.0);

protected:
    /* compute the functional f at a single vertex */
    virtual real_t fv(index_t v, const value_t* Xv) = 0; 

    /* compute graph contour length; use reduced edges and reduced weights */
    real_t compute_graph_d0();

    /* compute objective functional */
    virtual real_t compute_f();
    real_t compute_objective() override;

    /**  greedy splitting  **/
    /* rough estimate of the number of operations for split step;
     * useful for estimating the number of parallel threads */
    uintmax_t split_complexity() override;
    void split_component(comp_t rv, Maxflow<index_t, real_t>* maxflow)
        override;

    comp_t K; // number of alternative values in the split
    int split_iter_num; // number of partition-and-update iterations
    real_t split_damp_ratio; // split damping along iterations

    /* manage alternative values for a given component;
     * altX is a D-by-K array containing alternatives;
     * initialize usually with k-means;
     * update usually use some kind of averaging, and must flag in some way
     * alternative values which are no longer competing (i.e. associated to no
     * vertex), which can be checked with is_split_value */
    virtual void init_split_values(comp_t rv, value_t* altX) = 0;
    virtual void update_split_values(comp_t rv, value_t* altX) = 0;
    virtual bool is_split_value(value_t altX) = 0;
    /* rough estimate of the number of operations for initializing and
     * updating the split values */
    virtual uintmax_t split_values_complexity() = 0;

    /**  merging components  **/

    /* during the merging step, merged components are stored as chains, see
     * header `cut_pursuit.hpp` for details */

    /* the strategy is to compute the gain on the functional for the merge of
     * each reduced edge, and accept greedily the candidates with greatest
     * positive gain;
     * one could store the candidates in a priority queue, but the benefit is
     * not substantial since each merge might affect the others, hence a pass
     * on all remaining edges is necessary after each merge anyway;
     * to avoid unnecessary recomputation, positive merge gains and
     * corresponding values are stored;
     * to take additional information into account, override the virtual merge
     * update methods
     TODO: rewrite */
    struct Merge_info
    {
        size_t D;

        comp_t re; // the edge to be removed if merge 
        comp_t ru, rv; // the components concerned by the merge

        real_t gain; // the gain on the functional if the components are merged
        value_t* value; // the value taken by the components if they are merged
        
        Merge_info(size_t D = 0);
        Merge_info(const Merge_info&);
        ~Merge_info();
    };

    /* update information of the given merge candidate in the list;
     * merge information must be created with new and destroyed with delete;
     * negative gain values might still get accepted; for inacceptable gain,
     * do not create (or destroy if it exists) the merge information and flag
     * it with a null pointer;
     * NOTA: it might be necessary to take into account previous merges stored
     * in the merge chains, see header `cut_pursuit.hpp` for details
     TODO: rewrite */
    virtual void update_merge_info(Merge_info&) = 0;

    /* rough estimate of the number of operations for updating all candidates;
     * useful for estimating the number of parallel threads */
    virtual uintmax_t update_merge_complexity() = 0;

    /* accept the given merge candidate;
     * the root of the resulting chain will be the component in the chains
     * with lowest index, and assigned to the parameter ru; the root of the
     * other chain in the merge is assigned to rv;
     * see header `cut_pursuit.hpp` for details
     TODO: rewrite */
    virtual comp_t accept_merge(const Merge_info&);

    /**  type resolution for base template class members  **/
    using Cp<real_t, index_t, comp_t>::rX;
    using Cp<real_t, index_t, comp_t>::last_rX;
    using Cp<real_t, index_t, comp_t>::V;
    using Cp<real_t, index_t, comp_t>::E;
    using Cp<real_t, index_t, comp_t>::D;
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
    using Cp<real_t, index_t, comp_t>::is_saturated;
    using Cp<real_t, index_t, comp_t>::reduced_edge_weights;
    using Cp<real_t, index_t, comp_t>::reduced_edges;
    using Cp<real_t, index_t, comp_t>::saturated_vert;
    using Cp<real_t, index_t, comp_t>::get_merge_chain_root;
    using Cp<real_t, index_t, comp_t>::merge_components;
    using Cp<real_t, index_t, comp_t>::malloc_check;
    using Cp<real_t, index_t, comp_t>::realloc_check;
    using Cp<real_t, index_t, comp_t>::real_inf;

private:

    /* compute the merge chains and return the number of effective merges */
    comp_t compute_merge_chains() override;
    /* auxiliary functions for merge */
    void delete_merge_candidate(index_t re);
    void select_best_merge_candidate(index_t re, real_t* best_gain,
        index_t* best_edge);
    Merge_info reserved_merge_info;

    /**  type resolution for base template class members  **/
    using Cp<real_t, index_t, comp_t>::maxflow_complexity;
    using Cp<real_t, index_t, comp_t>::is_bind;
};

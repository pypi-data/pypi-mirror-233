# `InferredObservation` from `...ComposedOf` and `...EquivalentTo` relations

The "Y" algorithm follows these steps:

- `y_unify_elements`: renaming to use the same equivalence/composition rules for all dimensions
- `y_ordering`: selecting an order among the 'components' of each 'composite'
- `y_parallel_world_init`: initialising utility atoms
- `y_empty_observations`: identifying missing observations for each component
- `y_missing_measurement`: handling observations without a `measurement` value
- `y_parallel_world`: creating basic atoms for equivalence/composition computation in a new named graph
- `y_composition_tree`: computing composition (defining 'partial observations' tree)
- `y_equivalence`: computing equivalence (defining `ufu:elementDefinedByEquivalence` properties)
- `y_connected_members`: identifying observations aggregated for each new inferred observation via composition (used for 'was derived from' and bounds in next steps)
- `y_connected_wdf`: computing 'was derived from' for new inferred observation via composition
- `y_connected_bounds`: computing the bounds of each new inferred observation via composition
- `y_infer_new_obs`: inferring the newly computed observations in the default named graph
- stats:
  - `y_i_stats`: info before composition-equivalence
  - `y_m_stats`: info after initialisation (i.e., 'parallel world') for composition-equivalence
  - `y_f_stats`: info after composition-equivalence


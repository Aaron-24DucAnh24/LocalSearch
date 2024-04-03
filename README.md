1. **State space**:
   The current position (Cartesian coordinate of the agent) on the 2-d image.
1. **Objective function**:
   z = the brightness of certain point on the image.
   z ∈ [0, 255] and z ∈ N
1. **Actions**
   Agent can moves in 8 directions(vertically, horizontally, diagonally)
1. **Transition model**
   next(state) = (state.x+Δx, state.y+Δy)
   whereas Δx≠0, Δy≠0 (excluding the case agent does not make a move)

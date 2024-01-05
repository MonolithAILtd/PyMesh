#pragma once

#include "Octree.h"
#include <Core/EigenTypedef.h>

namespace PyMesh {
class Manifold {
public:
  Manifold();
  ~Manifold();
  void run(int depth);
  void setMesh(const MatrixFr &vertices, const MatrixIr &faces) {
    V_ = vertices;
    F_ = faces;
  }
  MatrixIr getManifoldFaces() const { return MF_; }
  MatrixFr getManifoldVertices() const { return MV_; }

protected:
  void BuildTree(int resolution);
  void CalcBoundingBox();
  void ConstructManifold();
  bool SplitGrid(const std::vector<Vector4I> &nface_indices,
                 std::map<GridIndex, int> &vcolor,
                 std::vector<Vector3F> &nvertices,
                 std::vector<std::set<int>> &v_faces,
                 std::vector<Vector3I> &triangles);

private:
  Octree *tree_;
  Vector3F min_corner_, max_corner_;
  MatrixFr V_, MV_;
  MatrixIr F_, MF_;

  std::vector<Vector3F> vertices_;
  std::vector<Vector3I> face_indices_;
  std::vector<GridIndex> v_info_;
};
} // namespace PyMesh

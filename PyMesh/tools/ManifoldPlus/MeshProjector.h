#pragma once

#include <igl/AABB.h>
#include <vector>

#include <Core/EigenTypedef.h>
using namespace PyMesh;

class MeshProjector {
public:
  MeshProjector();
  void ComputeHalfEdge();
  void ComputeIndependentSet();
  void UpdateFaceNormal(int i);
  void UpdateVertexNormal(int i, int conservative);
  void UpdateVertexNormals(int conservative);
  void IterativeOptimize(Float len, bool initialized = false);
  void AdaptiveRefine(Float len, Float ratio = 0.1);
  void EdgeFlipRefine(std::vector<int> &candidates);
  void Project(const MatrixFr &V, const MatrixIr &F, MatrixFr &out_V,
               MatrixIr &out_F);
  void UpdateNearestDistance();
  int BoundaryCheck();
  void SplitVertices();
  void OptimizePosition(int v, const Vector3F &target_p, Float len,
                        bool debug = false);
  void OptimizeNormal(int i, const Vector3F &vn, const Vector3F &target_vn);
  void OptimizeNormals();
  void PreserveSharpFeatures(Float len_thres);
  // void Highlight(int id, Float len);
  void Sanity(const char *log);

  bool IsNeighbor(int v1, int v2);

private:
  std::vector<std::vector<int>> vertex_groups_;

  igl::AABB<MatrixFr, 3> tree_;
  MatrixFr V_, out_V_, target_V_, out_N_, out_FN_;
  MatrixIr F_, out_F_;
  VectorI V2E_, E2E_;

  VectorF sqrD_;
  VectorI I_;

  std::vector<int> sharp_vertices_;
  std::vector<Vector3F> sharp_positions_;

  int num_V_, num_F_;

  std::vector<int> active_vertices_, active_vertices_temp_;
  std::vector<std::pair<Float, int>> indices_;
  int num_active_;
};

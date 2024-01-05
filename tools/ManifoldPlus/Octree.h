#pragma once
#include <list>
#include <map>
#include <set>
#include <vector>

#include "GridIndex.h"

class Octree {
public:
  Octree();
  Octree(const Vector3F min_c, const Vector3F max_c, const MatrixIr &faces);
  Octree(const Vector3F &min_c, const Vector3F &volume_size);
  ~Octree();

  bool IsExterior(const Vector3F &p);

  bool Intersection(int face_index, const Vector3F &min_corner,
                    const Vector3F &size, const MatrixFr &V);

  void Split(const MatrixFr &V);
  void BuildConnection();
  void ConnectTree(Octree *l, Octree *r, int dim);
  void ConnectEmptyTree(Octree *l, Octree *r, int dim);

  void ExpandEmpty(std::list<Octree *> &empty_list,
                   std::set<Octree *> &empty_set, int dim);

  void BuildEmptyConnection();

  void ConstructFace(const Vector3I &start, std::map<GridIndex, int> *vcolor,
                     std::vector<Vector3F> *vertices,
                     std::vector<Vector4I> *faces,
                     std::vector<std::set<int>> *v_faces);

  Vector3F min_corner_, volume_size_;
  int level_;
  int number_;
  int occupied_;
  int exterior_;

  Octree *children_[8];
  Octree *connection_[6];
  Octree *empty_connection_[6];
  std::list<Octree *> empty_neighbors_;

  std::vector<Vector3I> F_;
  std::vector<int> Find_;
};

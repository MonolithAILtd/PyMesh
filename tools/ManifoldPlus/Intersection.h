#pragma once

#include <Core/EigenTypedef.h>
using namespace PyMesh;

int TriBoxOverlap(float boxcenter[3], float boxhalfsize[3],
                  float triverts[3][3]);

int PlaneIntersect(const Vector3F &p0, const Vector3F &n0, const Vector3F &p1,
                   const Vector3F &n1, Vector3F *o, Vector3F *t);

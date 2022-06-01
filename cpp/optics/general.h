// geometrical-ray-tracing: Program to perform geometrical ray tracing
// Copyright (C) 2022  Tom Spencer (tspencerprog@gmail.com)

// This file is part of geometrical-ray-tracing

// geometrical-ray-tracing is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.


// Generic useful functions and type aliases
//
#pragma once
#define _USE_MATH_DEFINES  // Need for definition of M_PI
#include <cmath>
#include <array>
#include <limits>
#include <memory>
#include <string>
#include <utility>
#include <vector>

constexpr double infinity = std::numeric_limits<double>::infinity();

class Component;  // Forward declare the Component class
class Ray;

// Type aliases for the length two std::array and component vector
using arr = std::array<double, 2>;
using comp_list = std::vector<std::shared_ptr<Component>>;

// Forward declarations for tracing functions

// Determines the nect index in c of the next component the ray hits and the time it hits
// Returns time of infinity if no component is next to interact
template <typename T>
std::pair<size_t, double> next_component(const T &c, const Ray* r);

// Traces an individual ray for n interactions
template <typename T>
void trace_ray(const T &c, Ray* ry, int n, bool fill_up = true);

template <typename T>
// Traces a vector of rays through the components
void trace(const T &c, std::vector<Ray*> &rays, int n, bool fill_up = true);


// Adds a component to the vector to the vector vec
template <typename T>
void add_component(comp_list &vec, T c)
{
	vec.push_back(std::make_shared<T>(c));
}

// Saves rays to file
void save_rays(std::vector<Ray> &rays, std::string path);

// Save components to file
void save_components(comp_list &comps, std::string path);

// Helper functions

// Rotates the coordinates by alpha (rotates axis, not point)
arr rotate(const arr &r, const double theta);

// Absolute comparison between v1 and v2
inline bool is_close(double v1, double v2, double atol = 1e-8)
{
	return abs(v1 - v2) < atol;
}

// Renormalises vector whose magnitude is close to 1 using first order Taylor series
// for 1/sqrt(abs(vec))
void renorm_unit_vec(arr &v);

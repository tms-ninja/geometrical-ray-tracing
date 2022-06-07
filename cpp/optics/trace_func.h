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


// Contains the tracing functions and function to add component to comp_list
// 
#pragma once
#include "general.h"
#include "Component.h"
#include "Ray.h"
#include <fstream>
#include <string>
#include <tuple>

// Determines the index in c of the next component the ray hits and the time it hits
// Returns time of infinity if no component is next to interact
template <typename T>
std::pair<size_t, double> next_component(const T &c, const Ray* r);

// Traces an individual ray for n interactions
template <typename T>
void trace_ray(const T &c, Ray* ry, int n, bool fill_up);

// Traces a vector of rays through the components
// Don't need to redefine 
template <typename T>
void trace(const T &c, std::vector<Ray*> &rays, int n, bool fill_up);

// Explicity initiate these template types to allows component list to contain either unique_ptr or raw pointers
template void trace(const std::vector<std::shared_ptr<Component>> &c, std::vector<Ray*> &rays, int n, bool fill_up);
//template void trace(const std::vector<std::unique_ptr<Component>> &c, std::vector<Ray*> &rays, int n, bool fill_up);
template void trace(const std::vector<Component*> &c, std::vector<Ray*> &rays, int n, bool fill_up);
 
// Saves rays to file
void save_rays(std::vector<Ray> &rays, std::string path);

// Save components to file
void save_components(comp_list &comps, std::string path);

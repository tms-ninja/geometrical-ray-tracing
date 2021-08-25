// Contains the tracing functions and function to add component to comp_list
// 
#pragma once
#include "general.h"
#include "Component.h"
#include "Ray.h"
#include <fstream>
#include <string>

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

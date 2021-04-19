// Generic useful functions and type aliases
//
#pragma once
#define _USE_MATH_DEFINES  // Need for definition of M_PI
#include <cmath>
#include <array>
#include <memory>
#include <vector>

class Component;  // Forward declare the Component class
class Ray;

// Type aliases for the length two std::array and component vector
using arr = std::array<double, 2>;
using comp_list = std::vector<std::unique_ptr<Component>>;

int next_component(const std::vector<double> &t);

// Forward declarations for tracing functions

// Traces an individual ray for n interactions
template <typename T>
void trace_ray(const T &c, Ray &ry, int n, bool fill_up = true);

template <typename T>
// Traces a vector of rays through the components
void trace(const T &c, std::vector<Ray> &rays, int n, bool fill_up = true);


// Adds a component to the vector to the vector vec
template <typename T>
void add_component(comp_list &vec, T c)
{
	vec.push_back(std::make_unique<T>(c));
}

// Saves rays to file
void save_rays(std::vector<Ray> &rays, std::string path);

// Save components to file
void save_components(comp_list &comps, std::string path);
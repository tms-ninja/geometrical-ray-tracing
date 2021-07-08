// Class to describe component composed of multiple sub-components
// E.g. triangluar prism can be described as three planar boundaries where refraction occurs
#pragma once
#include "Component.h"
#include "general.h"
#include <utility>
#include <vector>

class Complex_Component :
	public Component
{
public:
	comp_list comps;

	// Hit methods
	virtual double test_hit(Ray* ry) const override;
	virtual void hit(Ray* ry, int n = 1) const override;

	// Printing
	virtual void print(std::ostream& os) const override;

	// Add method for adding components
	template <typename T>
	void add(T c)
	{
		comps.push_back(std::make_shared<T>(c));
	}
};



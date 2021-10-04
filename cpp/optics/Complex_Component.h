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

	Complex_Component() = default;

	// Need to provide custom copy constructor/assignment as shared_ptr won't produce and independent
	// copy when its copy constructor/assignment operator are invoked
	Complex_Component(const Complex_Component& c);
	Complex_Component& operator=(const Complex_Component c);


	// Move constructors/assignment operators are trivial as we'll be invoking the vector's move
	// constructor/assignment operators
	Complex_Component(Complex_Component&&) = default;
	Complex_Component& operator=(Complex_Component&&) = default;

	friend void swap(Complex_Component& c1, Complex_Component &c2);


	// Hit methods
	virtual double test_hit(Ray* ry) const override;
	virtual void hit(Ray* ry, int n = 1) const override;

	virtual Complex_Component* clone() const override;


	// Printing
	virtual void print(std::ostream& os) const override;

	// Add method for adding components
	template <typename T>
	void add(T c)
	{
		comps.push_back(std::make_shared<T>(c));
	}
};



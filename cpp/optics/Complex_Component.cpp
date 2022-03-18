#include "Complex_Component.h"

Complex_Component::Complex_Component(const Complex_Component &c)
{
	this->comps.reserve(c.comps.size());

	for (auto& ptr : c.comps)
	{
		// Ensure the raw pointer returned by ptr->clone() is wrapped up
		// in a smart pointer so if push_back() throws, the memory isn't
		// leaked
		this->comps.push_back(std::shared_ptr<Component>(ptr->clone()));
	}
}

Complex_Component & Complex_Component::operator=(Complex_Component c)
{
	swap(*this, c);  // Use copy-swap idiom

	return *this;
}

void swap(Complex_Component & c1, Complex_Component & c2)
{
	std::swap(c1.comps, c2.comps);
}

double Complex_Component::test_hit(const Ray* ry) const
{
	double t;

	std::tie(std::ignore, t) = next_component(comps, ry);

	return t;
}

void Complex_Component::hit(Ray* ry, int n) const
{
	trace_ray(comps, ry, n);
}

Complex_Component* Complex_Component::clone() const
{
	return new Complex_Component{ *this };
}

void Complex_Component::print(std::ostream & os) const
{
	os << "Prinitng not implemented for Complex_Component yet!";
}

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

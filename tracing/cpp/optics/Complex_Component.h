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


// Class to describe an optical component composed of multiple sub-components
// E.g. triangluar prism can be described as three planar boundaries where refraction occurs
//
#pragma once
#include "Component.h"
#include "general.h"
#include <tuple>
#include <utility>
#include <vector>

namespace optics
{
	class Complex_Component :
		public Component
	{
	public:
		// Sub-components the Complex_Component is composed from
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

		friend void swap(Complex_Component& c1, Complex_Component& c2);


		// Hit methods
		virtual double test_hit(const Ray* ry) const override;
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
}

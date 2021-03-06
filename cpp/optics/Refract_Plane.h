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


// Describes a plane at which refraction occurs
//
#pragma once
#include "Plane.h"
#include "trace_func.h"

namespace optics
{
	class Refract_Plane :
		public Plane
	{
	public:
		double n1, n2;

		Refract_Plane(arr start, arr end, double n1 = 1.0, double n2 = 1.0);

		// Hit function
		virtual void hit(Ray* ry, int n) const override;

		virtual Refract_Plane* clone() const override;
	};
}

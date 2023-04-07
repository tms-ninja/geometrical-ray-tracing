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


// Describes a plane that 'absorbs' rays which hit it. Further tracing of 
// rays that hit Screen_Plane will not occur.
//
#pragma once
#include "Plane.h"

namespace optics
{
	class Screen_Plane :
		public Plane
	{
	public:

		Screen_Plane(arr start, arr end);

		// Hit function
		virtual void hit(Ray* ry, int n) const override;

		virtual Screen_Plane* clone() const override;
	};
}

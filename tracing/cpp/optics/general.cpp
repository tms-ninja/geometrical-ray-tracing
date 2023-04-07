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


#pragma once
#include "general.h"

namespace optics
{
	arr rotate(const arr& r, const double theta)
	{
		double top{ cos(theta) * r[0] + sin(theta) * r[1] };
		double bottom{ -sin(theta) * r[0] + cos(theta) * r[1] };

		return { top, bottom };
	}

	void renorm_unit_vec(arr& v)
	{
		double v_mag_sq, x, fact;

		v_mag_sq = v[0] * v[0] + v[1] * v[1];

		// using Taylor expansion for 1/sqrt(x) around x=1
		x = v_mag_sq - 1.0;

		fact = 1.0 - x / 2.0;//  +3.0*x*x / 8.0;

		v[0] *= fact;
		v[1] *= fact;
	}
}

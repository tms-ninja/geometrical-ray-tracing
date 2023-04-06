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


#include "Ray.h"

namespace optics
{

	Ray::Ray(arr init, arr v)
		: continue_tracing(true)
	{
		pos.push_back(init);
		Ray::v = v;
	}

	std::ostream& operator<<(std::ostream& os, const Ray& ry)
	{
		for (int xy = 0; xy < 2; ++xy)
		{
			for (std::size_t i = 0; i < ry.pos.size() - 1; ++i)  // Iterate through all x values except the last one
			{
				os << ry.pos[i][xy] << '\t';
			}

			os << ry.pos[ry.pos.size() - 1][xy] << '\n';
		}

		return os;
	}

	void Ray::reset(const arr& new_v)
	{
		v = new_v;
		pos.resize(1);
	}

	void Ray::reset(const arr& new_v, const arr& new_start)
	{
		v = new_v;

		pos.resize(1);
		pos[0] = new_start;
	}
}

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


#include "trace_func.h"

namespace optics 
{
	template<typename T>
	std::pair<size_t, double> next_component(const T& c, const Ray* ry)
	{
		double current_t;
		double best_t{ infinity };
		size_t best_ind{ 0 };

		for (std::size_t ind = 0; ind < c.size(); ++ind)
		{
			current_t = c[ind]->test_hit(ry);

			if (current_t < best_t)
			{
				best_t = current_t;
				best_ind = ind;
			}
		}

		return { best_ind, best_t };
	}

	template <typename T>
	void trace_ray(const T& c, Ray* ry, int n, bool fill_up)
	{
		if (fill_up)
			ry->pos.reserve(ry->pos.size() + n);

		for (int i = 0; i < n; ++i)
		{
			// Ensure normalisation of ry->v does not drift from 1
			renorm_unit_vec(ry->v);

			// Now do tracing
			// Determine which, if any is the next component
			size_t next_ind;
			double t;
			bool found;

			std::tie(next_ind, t) = next_component(c, ry);
			found = t != infinity;

			if (found) // work out next interaction
			{
				c[next_ind]->hit(ry);
			}

			arr& r{ ry->pos.back() };  // last position of ray

			// no more interactions or hit a screen and should stop tracing
			if (!found || !ry->continue_tracing)
			{
				const arr end = { r[0] + (ry->continue_tracing ? ry->v[0] : 0.0)
								, r[1] + (ry->continue_tracing ? ry->v[1] : 0.0) };

				if (fill_up)  // fill up to desired n
				{
					for (int j = 0; j < n - i; ++j)
					{
						ry->pos.push_back(end);
					}
				}
				else if (ry->continue_tracing)  // only add another if continue tracing
					ry->pos.push_back(end);  // show result of last interaction

				return;  // Exit the function as we have nothing else to do
			}
		}
	}

	template <typename T>
	void trace(const T& c, std::vector<Ray*>& rays, int n, bool fill_up)
	{
		for (Ray* r : rays)
			trace_ray(c, r, n, fill_up);
	}

	arr compute_new_pos(const Ray& ry, const double t)
	{
		arr newPos;

		const arr& r = ry.pos.back();
		const arr& v = ry.v;

		// Compute new position
		for (int i = 0; i < 2; ++i)
			newPos[i] = (r[i] + v[i] * t);

		return newPos;
	}

	void reflect_ray(Ray& ry, const arr n_vec)
	{
		arr& v = ry.v;

		// Compute new direction
		double v_dot_n{ v[0] * n_vec[0] + v[1] * n_vec[1] };

		for (int i = 0; i < 2; ++i)
			v[i] -= 2 * v_dot_n * n_vec[i];
	}

	void refract_ray(Ray& ry, const arr n_vec, const double n1, const double n2)
	{
		arr& v = ry.v;
		double ni, nf;

		double vi_dot_n{ v[0] * n_vec[0] + v[1] * n_vec[1] };

		if (vi_dot_n > 0.0)
		{
			ni = n2;
			nf = n1;
		}
		else
		{
			ni = n1;
			nf = n2;
		}

		double gamma{ (n_vec[0] * v[1] - n_vec[1] * v[0]) * ni / nf };
		double disc{ 1 - gamma * gamma };

		// If discriminant is less than zero, we have reflection instead of refraction
		if (disc < 0.0)
		{
			v[0] -= 2 * vi_dot_n * n_vec[0];
			v[1] -= 2 * vi_dot_n * n_vec[1];

			return;
		}

		// we are performing refraction
		disc = std::sqrt(disc);

		// Either side of +/- of resulting speeds
		double disc_term[2];

		disc_term[0] = n_vec[0] * disc;
		disc_term[1] = n_vec[1] * disc;

		arr D{ n_vec[1], -n_vec[0] };

		double vi_dot_D{ v[0] * D[0] + v[1] * D[1] };

		v[0] = -n_vec[1] * gamma + disc_term[0];
		v[1] = n_vec[0] * gamma + disc_term[1];

		double vf_dot_n{ v[0] * n_vec[0] + v[1] * n_vec[1] };
		double vf_dot_D{ v[0] * D[0] + v[1] * D[1] };

		if (std::signbit(vi_dot_n) != std::signbit(vf_dot_n) || std::signbit(vi_dot_D) != std::signbit(vf_dot_D))
		{
			v[0] -= 2 * disc_term[0];
			v[1] -= 2 * disc_term[1];
		}
	}

	void save_rays(std::vector<Ray>& rays, std::string path)
	{
		std::ofstream write_file(path);

		for (Ray& r : rays)
			write_file << r;
	}

	void save_components(comp_list& comps, std::string path)
	{
		std::ofstream write_file(path);

		for (auto& c : comps)
			write_file << *c;  // Note each element is std::unique_ptr<Component>, so need to dereference c
	}


}

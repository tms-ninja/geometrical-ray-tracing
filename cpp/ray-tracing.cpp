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


// Contains functions for testing performance of different components
// Not used for tracing 
//
#define _USE_MATH_DEFINES  // Need for definition of M_PI
#include <cmath>
#include <iostream>
#include <iomanip>
#include <chrono>

#include "optics/general.h"
#include "optics/Mirror_Sph.h"
#include "optics/Mirror_Plane.h"
#include "optics/Refract_Sph.h"
#include "optics/Refract_Plane.h"

void test_Mirror_Sph()
{
	using optics::Ray;
	optics::comp_list c;

	optics::add_component(c, optics::Mirror_Sph({ 0.0, 0.0 }, 10.0, 0.0, 2 * M_PI));

	auto begin = std::chrono::steady_clock::now();

	// Define the list of rays and add
	for (size_t i = 0; i < 70000; i++)
	{
		std::vector<Ray> rays;
		double theta{ M_PI / 180.0 * 60.0 };


		rays.push_back(Ray({ 1.0, 0 }, { cos(theta), sin(theta) }));

		std::vector<Ray*> ray_ptrs;

		for (auto &r : rays)
			ray_ptrs.push_back(&r);

		optics::trace(c, ray_ptrs, 100);
	}

	auto end = std::chrono::steady_clock::now();

	std::cout << "Total duration: " << std::chrono::duration_cast<std::chrono::microseconds>(end - begin).count() / 1000 << "[ms]" << std::endl;
}

void test_Mirror_Plane()
{
	using optics::Ray;
	optics::comp_list c;

	optics::add_component(c, optics::Mirror_Plane({ -10.0, 10.0 }, { 10.0, 10.0 }));
	optics::add_component(c, optics::Mirror_Plane({ 10.0, 10.0 }, { 10.0, -10.0 }));
	optics::add_component(c, optics::Mirror_Plane({ 10.0, -10.0 }, { -10.0, -10.0 }));
	optics::add_component(c, optics::Mirror_Plane({ -10.0, -10.0 }, { -10.0, 10.0 }));

	auto begin = std::chrono::steady_clock::now();

	// Define the list of rays and add
	for (size_t i = 0; i < 400000; i++)
	{
		std::vector<Ray> rays;
		double theta{ M_PI / 180.0 * 60.0 };

		rays.push_back(Ray({ 1.0, 0 }, { cos(theta), sin(theta) }));

		std::vector<Ray*> ray_ptrs;

		for (auto &r : rays)
			ray_ptrs.push_back(&r);

		optics::trace(c, ray_ptrs, 100);
	}

	auto end = std::chrono::steady_clock::now();

	std::cout << "Total duration: " << std::chrono::duration_cast<std::chrono::microseconds>(end - begin).count() / 1000 << "[ms]" << std::endl;
}

void test_Refract_Sph()
{
	using optics::Ray;
	optics::comp_list c;

	// spherical mirror to keep rays trapped
	optics::add_component(c, optics::Mirror_Sph({ 0.0, 0.0 }, 10.0, 0.0, 2 * M_PI));

	std::vector<double> R = { 3.0, 5.0, 7.0, 9.0 };
	std::vector<double> n_in = { 1.3, 1.4, 1.5, 1.6 };
	std::vector<double> n_out = { 1.0, 1.3, 1.4, 1.5 };

	for (size_t i = 0; i < R.size(); i++)
	{
		optics::add_component(c, optics::Refract_Sph({ 0.0, 0.0 }, R[i], 0.0, 2 * M_PI, n_out[i], n_in[i]));
	}

	auto begin = std::chrono::steady_clock::now();

	// Define the list of rays and add
	for (size_t i = 0; i < 40000; i++)
	{
		std::vector<Ray> rays;
		double theta{ M_PI / 180.0 * 60.0 };

		rays.push_back(Ray({ 1.0, 0 }, { cos(theta), sin(theta) }));

		std::vector<Ray*> ray_ptrs;

		for (auto &r : rays)
			ray_ptrs.push_back(&r);

		optics::trace(c, ray_ptrs, 100);
	}

	auto end = std::chrono::steady_clock::now();

	std::cout << "Total duration: " << std::chrono::duration_cast<std::chrono::microseconds>(end - begin).count() / 1000 << "[ms]" << std::endl;
}

void test_Refract_Plane()
{
	using optics::Ray;
	optics::comp_list c;

	// Mirrors so ray doesn't escape
	optics::add_component(c, optics::Mirror_Plane({ -10.0, 10.0 }, { 10.0, 10.0 }));
	optics::add_component(c, optics::Mirror_Plane({ 10.0, 10.0 }, { 10.0, -10.0 }));
	optics::add_component(c, optics::Mirror_Plane({ 10.0, -10.0 }, { -10.0, -10.0 }));
	optics::add_component(c, optics::Mirror_Plane({ -10.0, -10.0 }, { -10.0, 10.0 }));

	double L_vals[] = { 5.0, 7.0, 9.0 };
	double n_in[] = { 1.2, 1.3, 1.4 };
	double n_out[] = { 1.0, 1.2, 1.3 };
	double L;

	for (size_t i = 0; i < 3; i++)
	{
		L = L_vals[i];

		optics::add_component(c, optics::Refract_Plane({ -L, L }, { L, L }, n_out[i], n_in[i]));
		optics::add_component(c, optics::Refract_Plane({ L, L }, { L, -L }, n_out[i], n_in[i]));
		optics::add_component(c, optics::Refract_Plane({ L, -L }, { -L, -L }, n_out[i], n_in[i]));
		optics::add_component(c, optics::Refract_Plane({ -L, -L }, { -L, L }, n_out[i], n_in[i]));
	}

	auto begin = std::chrono::steady_clock::now();

	// Define the list of rays and add
	for (size_t i = 0; i < 70000; i++)
	{
		std::vector<Ray> rays;
		double theta{ M_PI / 180.0 * 60.0 };

		rays.push_back(Ray({ 1.0, 0 }, { cos(theta), sin(theta) }));

		std::vector<Ray*> ray_ptrs;

		for (auto &r : rays)
			ray_ptrs.push_back(&r);

		optics::trace(c, ray_ptrs, 100);
	}

	auto end = std::chrono::steady_clock::now();

	std::cout << "Total duration: " << std::chrono::duration_cast<std::chrono::microseconds>(end - begin).count() / 1000 << "[ms]" << std::endl;

}

void test_concentric_Mirror_Sph()
{
	using optics::Ray;
	optics::comp_list c;

	optics::add_component(c, optics::Mirror_Sph({ 0.0, 0.0 }, 10.0, 0.0, 2 * M_PI));
	optics::add_component(c, optics::Mirror_Sph({ 0.0, 0.0 }, 5.0, 0.0, 2 * M_PI));

	auto begin = std::chrono::steady_clock::now();

	// Define the list of rays and add
	std::vector<Ray> rays;
	double theta{ M_PI / 180.0 * 10.0 };


	rays.push_back(Ray({ -8.0, 0 }, { cos(theta), sin(theta) }));

	std::vector<Ray*> ray_ptrs;

	for (auto &r : rays)
		ray_ptrs.push_back(&r);

	optics::trace(c, ray_ptrs, 25);

	auto end = std::chrono::steady_clock::now();

	std::cout << "Total duration: " << std::chrono::duration_cast<std::chrono::microseconds>(end - begin).count() / 1000 << "[ms]" << std::endl;

	std::cout << rays[0];
}

int main()
{
	std::cout << std::fixed << "Program started!\n";

	test_Refract_Plane();

	// Save rays and components
	//std::cout << rays[0];

	std::cout << "End of program\n";
}

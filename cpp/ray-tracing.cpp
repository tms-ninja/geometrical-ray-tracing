// Ray tracing program written to learn about polymorphism in C++
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
	comp_list c;

	add_component(c, Mirror_Sph({ 0.0, 0.0 }, 10.0, 0.0, 2 * M_PI));

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

		trace(c, ray_ptrs, 100);
	}

	auto end = std::chrono::steady_clock::now();

	std::cout << "Total duration: " << std::chrono::duration_cast<std::chrono::microseconds>(end - begin).count() / 1000 << "[ms]" << std::endl;
}

void test_Mirror_Plane()
{
	comp_list c;

	add_component(c, Mirror_Plane({ -10.0, 10.0 }, { 10.0, 10.0 }));
	add_component(c, Mirror_Plane({ 10.0, 10.0 }, { 10.0, -10.0 }));
	add_component(c, Mirror_Plane({ 10.0, -10.0 }, { -10.0, -10.0 }));
	add_component(c, Mirror_Plane({ -10.0, -10.0 }, { -10.0, 10.0 }));

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

		trace(c, ray_ptrs, 100);
	}

	auto end = std::chrono::steady_clock::now();

	std::cout << "Total duration: " << std::chrono::duration_cast<std::chrono::microseconds>(end - begin).count() / 1000 << "[ms]" << std::endl;
}

void test_Refract_Sph()
{
	comp_list c;

	// spherical mirror to keep rays trapped
	add_component(c, Mirror_Sph({ 0.0, 0.0 }, 10.0, 0.0, 2 * M_PI));

	std::vector<double> R = { 3.0, 5.0, 7.0, 9.0 };
	std::vector<double> n_in = { 1.3, 1.4, 1.5, 1.6 };
	std::vector<double> n_out = { 1.0, 1.3, 1.4, 1.5 };

	for (size_t i = 0; i < R.size(); i++)
	{
		add_component(c, Refract_Sph({ 0.0, 0.0 }, R[i], 0.0, 2 * M_PI, n_out[i], n_in[i]));
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

		trace(c, ray_ptrs, 100);
	}

	auto end = std::chrono::steady_clock::now();

	std::cout << "Total duration: " << std::chrono::duration_cast<std::chrono::microseconds>(end - begin).count() / 1000 << "[ms]" << std::endl;
}

void test_Refract_Plane()
{
	comp_list c;

	// Mirrors so ray doesn't escape
	add_component(c, Mirror_Plane({ -10.0, 10.0 }, { 10.0, 10.0 }));
	add_component(c, Mirror_Plane({ 10.0, 10.0 }, { 10.0, -10.0 }));
	add_component(c, Mirror_Plane({ 10.0, -10.0 }, { -10.0, -10.0 }));
	add_component(c, Mirror_Plane({ -10.0, -10.0 }, { -10.0, 10.0 }));

	double L_vals[] = { 5.0, 7.0, 9.0 };
	double n_in[] = { 1.2, 1.3, 1.4 };
	double n_out[] = { 1.0, 1.2, 1.3 };
	double L;

	for (size_t i = 0; i < 3; i++)
	{
		L = L_vals[i];

		add_component(c, Refract_Plane({ -L, L }, { L, L }, n_out[i], n_in[i]));
		add_component(c, Refract_Plane({ L, L }, { L, -L }, n_out[i], n_in[i]));
		add_component(c, Refract_Plane({ L, -L }, { -L, -L }, n_out[i], n_in[i]));
		add_component(c, Refract_Plane({ -L, -L }, { -L, L }, n_out[i], n_in[i]));
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

		trace(c, ray_ptrs, 100);
	}

	auto end = std::chrono::steady_clock::now();

	std::cout << "Total duration: " << std::chrono::duration_cast<std::chrono::microseconds>(end - begin).count() / 1000 << "[ms]" << std::endl;

}

void test_concentric_Mirror_Sph()
{
	comp_list c;

	add_component(c, Mirror_Sph({ 0.0, 0.0 }, 10.0, 0.0, 2 * M_PI));
	add_component(c, Mirror_Sph({ 0.0, 0.0 }, 5.0, 0.0, 2 * M_PI));

	auto begin = std::chrono::steady_clock::now();

	// Define the list of rays and add
	std::vector<Ray> rays;
	double theta{ M_PI / 180.0 * 10.0 };


	rays.push_back(Ray({ -8.0, 0 }, { cos(theta), sin(theta) }));

	std::vector<Ray*> ray_ptrs;

	for (auto &r : rays)
		ray_ptrs.push_back(&r);

	trace(c, ray_ptrs, 25);

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

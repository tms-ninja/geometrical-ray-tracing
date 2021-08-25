// Ray tracing program written to learn about polymorphism in C++
//
#define _USE_MATH_DEFINES  // Need for definition of M_PI
#include <cmath>
#include <iostream>
#include <iomanip>
#include <chrono>

#include "optics\general.h"
#include "optics\Mirror_Sph.h"
#include "optics\Mirror_Plane.h"

int main()
{
	std::cout << std::fixed << "Program started!\n";

	//std::vector<std::unique_ptr<Component>> c;  // Define the list of components and add components
	comp_list c;


	//add_component(c, Mirror_Plane({ 0.0, 1.0 }, { 2.0, -1.0 }));
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

	// Save rays and components



	//std::cout << rays[0];

	std::cout << "End of program\n";
}

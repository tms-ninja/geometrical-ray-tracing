#include "trace_func.h"

// Traces an individual ray for n interactions
template <typename T>
void trace_ray(const T &c, Ray* ry, int n, bool fill_up)
{
	std::vector<double> t;  // Holds t values for each component, -1.0 if no interaction

	t.resize(c.size());

	for (int i = 0; i < n; ++i)
	{
		arr &r{ ry->pos.back() };  // last position of ray

		// Check for all interactions
		for (std::size_t cInd = 0; cInd < c.size(); ++cInd)
			t[cInd] = c[cInd]->test_hit(ry);

		size_t next_ind{ next_component(t) };

		if (next_ind == -1 && fill_up)  // no more interactions, fill up to desired n
		{
			const arr end = { r[0] + ry->v[0], r[1] + ry->v[1] };

			for (int j = 0; j < n - i; ++j)
			{
				ry->pos.push_back(end);
			}

			return;  // Exit the function as we have nothing else to do
		}
		else if (next_ind >= 0)  // work out next interaction
		{
			c[next_ind]->hit(ry);
		}
	}
}

// Traces a vector of rays through the components
template <typename T>
void trace(const T &c, std::vector<Ray*> &rays, int n, bool fill_up)
{
	for (Ray* r : rays)
		trace_ray(c, r, n, fill_up);
}

void save_rays(std::vector<Ray>& rays, std::string path)
{
	std::ofstream write_file(path);

	for (Ray &r : rays)
		write_file << r;
}

void save_components(comp_list & comps, std::string path)
{
	std::ofstream write_file(path);

	for (auto &c : comps)
		write_file << *c;  // Note each element is std::unique_ptr<Component>, so need to dereference c
}


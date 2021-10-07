#include "trace_func.h"


// Determines which component, if any, is the next one to interact
template<typename T>
std::pair<size_t, double> next_component(const T & c, const Ray * ry)
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

// Traces an individual ray for n interactions
template <typename T>
void trace_ray(const T &c, Ray* ry, int n, bool fill_up)
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

		arr &r{ ry->pos.back() };  // last position of ray

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


#include "Ray.h"

Ray::Ray(arr init, arr v)
: continue_tracing(true)
{
	pos.push_back(init);
	Ray::v = v;
}

std::ostream & operator<<(std::ostream & os, const Ray & ry)
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

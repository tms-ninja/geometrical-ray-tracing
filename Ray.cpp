#include "Ray.h"

Ray::Ray(arr init, arr v)
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

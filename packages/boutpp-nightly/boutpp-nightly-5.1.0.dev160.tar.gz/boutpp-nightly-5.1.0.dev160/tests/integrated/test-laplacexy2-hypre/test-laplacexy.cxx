/**************************************************************************
 * Testing Perpendicular Laplacian inversion using PETSc solvers
 *
 **************************************************************************
 * Copyright 2019 J.T. Omotani, B.D. Dudson
 *
 * Contact: Ben Dudson, bd512@york.ac.uk
 *
 * This file is part of BOUT++.
 *
 * BOUT++ is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * BOUT++ is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with BOUT++.  If not, see <http://www.gnu.org/licenses/>.
 *
 **************************************************************************/

#include <bout/bout.hxx>
#include <bout/constants.hxx>
#include <bout/derivs.hxx>
#include <bout/initialprofiles.hxx>
#include <bout/invert/laplacexy2_hypre.hxx>
#include <bout/options.hxx>

int main(int argc, char** argv) {

  BoutInitialise(argc, argv);

  LaplaceXY2Hypre laplacexy;

  // Solving equations of the form
  // Div(A Grad_perp(f)) + B*f = rhs
  // A*Laplace_perp(f) + Grad_perp(A).Grad_perp(f) + B*f = rhs
  Field2D f, a, b;

  initial_profile("f", f);
  initial_profile("a", a);
  initial_profile("b", b);

  // Apply boundary conditions to f, so the boundary cells match the way boundary
  // conditions will be applied to sol
  f.setBoundary("f");
  f.applyBoundary();

  ////////////////////////////////////////////////////////////////////////////////////////

  Field2D rhs = Laplace_perpXY(a, f) + b * f;

  laplacexy.setCoefs(a, b);

  Field2D guess = 0.0;
  Field2D sol = laplacexy.solve(rhs, guess);
  Field2D error = (f - sol) / f;
  Field2D absolute_error =
      abs(f - sol); // Absolute value of relative error: abs((f - sol)/f)
  BoutReal max_error = max(absolute_error, true);

  output << "Magnitude of maximum absolute error is " << max_error << endl;

  sol.getMesh()->communicate(sol);
  Field2D rhs_check = Laplace_perpXY(a, sol);

  using bout::globals::dump;

  dump.add(a, "a");
  dump.add(b, "b");
  dump.add(f, "f");
  dump.add(sol, "sol");
  dump.add(error, "error");
  dump.add(absolute_error, "absolute_error");
  dump.add(max_error, "max_error");
  dump.add(rhs, "rhs");
  dump.add(rhs_check, "rhs_check");

  dump.write();
  dump.close();

  MPI_Barrier(BoutComm::get()); // Wait for all processors to write data

  BoutFinalise();
  return 0;
}

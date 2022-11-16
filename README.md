# ViscoMet
Viscomet is a software for controlling, acquiring and plotting the data of the new portable field rotational viscometer for high-temperature melts**. It simultaneously acquires and displays the three fundamental parameters in real time to determine the viscosity of a medium: i.e. rotation speed, torque, and temperature.

The field rotational viscometer has been designed to measure the viscosity of lavas on the volcano flanks, but it could potentially also be used in various other settings such as glass industry. At one end a shear vane is immersed in the lava and at the other end, a motor rotates the shear vane. A torque sensor is placed between the two and measures the torque exerted by the molten phase on the shear vane that is proportional to viscosity. In addition, a thermocouple placed between the blades of the shear vane measures the temperature of the material. 

ViscoMet is not designed to deliver direct viscosity values, instead, it delivers the raw data of torque and rotation per minute that can then be converted by the user. Data processing has to be operated after acquisition on an independent system and following the wide-gap concentric cylinder theory of the Couette's rotating viscometer principle.

 **If you use Viscomet please cite the following reference **:

"Chevrel M.O., T. Latchimy, L. Batier and R. Delpoux. A new portable field rotational viscometer for high-temperature melts. Submitted to Reviews in Scientific Instrument. 16 Nov. 2022"

This article contains an overview of the conception, implementation, and validation of the portable field viscometer and additional information concerning the main components, data acquisition and applications.
# Installation 
This package needs Python 2 and additional packages:
* matplolib
* pyserial
* PyQt4
* thermocouples_reference  
# Help
The folder "html" contains the documentation of the software that is created  by doxygen.  
You just need to copy the entire folder and open the index.html inside.
# Author
* Thierry Latchimy (T.Latchimy@opgc.fr)
* CNRS OPGC, Université Clermont Auvergne
# License
* GNU General Public License v3.0
* Source code must be made available when the software is distributed.
* See the LICENSE file for details
* https://www.gnu.org/licenses/gpl-3.0.txt


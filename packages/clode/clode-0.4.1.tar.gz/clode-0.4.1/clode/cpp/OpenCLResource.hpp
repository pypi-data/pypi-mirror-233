/*
 * OpenCLResource.hpp
 *
 *  Copyright 2017 Patrick Fletcher <patrick.fletcher@nih.gov>
 * 
 * Inspired by openCLUtilities
 */

//TODO: more filters - max clock, max memory, extension available (eg. fp64), CL version, etc - How to apply multiple filters?

//TODO: store maps of (UsrNameStr, cl::Mem[Buffer,Image,etc]), (nameStr, cl::Kernel), (UsrNameStr, cl::Event), and member functions to enable operations with these
//TODO: with above, could wrap with mex function and Matlab cpp class wrapper => opencltoolbox

#ifndef OPENCL_RESOURCE_HPP_
#define OPENCL_RESOURCE_HPP_

#define CL_HPP_ENABLE_EXCEPTIONS
#define CL_HPP_MINIMUM_OPENCL_VERSION 120
#define CL_HPP_TARGET_OPENCL_VERSION 120
#define CL_HPP_CL_1_2_DEFAULT_BUILD
#define CL_HPP_ENABLE_PROGRAM_CONSTRUCTION_FROM_ARRAY_COMPATIBILITY
#include "OpenCL/cl2.hpp"

#include <string>
#include <vector>

typedef cl_device_type cl_deviceType;

enum cl_vendor
{
	VENDOR_ANY = 0,
	VENDOR_NVIDIA,
	VENDOR_AMD,
	VENDOR_INTEL
};

//struct to hold a reduced set of information about a device
typedef struct deviceInfo
{
	std::string name;
	std::string vendor;
	std::string version;
	cl_device_type devType;
	std::string devTypeStr;
	cl_uint computeUnits;
	cl_uint maxClock;
	size_t maxWorkGroupSize;
	cl_ulong deviceMemSize;
	cl_ulong maxMemAllocSize;
	std::string extensions;
	bool doubleSupport;
	cl_bool deviceAvailable;
} deviceInfo;

typedef struct platformInfo
{
	std::string name;
	std::string vendor;
	std::string version;
	std::vector<deviceInfo> device_info;
	unsigned int nDevices;
} platformInfo;

// A small convenience class to represent an OpenCL context with selected device(s) on a platform of interest. A command queue is also created for each device.
class OpenCLResource
{

	cl::Platform platform;
	platformInfo platform_info;
	cl::Context context;
	cl::Program program;

	//the following vectors will all contain one entry per device in the context
	std::vector<cl::Device> devices;
	std::vector<cl::CommandQueue> queues; //could have many queues per device...

	//TODO: figure out how to use events... one per queue? one per context? for syncing & barriers, out-of-order queues etc..
	//cl::Event event;

	//helper functions to get the desired platform and device(s), and create the context and command queues
	void getPlatformAndDevices(cl_deviceType type = CL_DEVICE_TYPE_ALL, cl_vendor vendor = VENDOR_ANY);
	void getPlatformAndDevices(unsigned int platformID, std::vector<unsigned int> deviceID); //cl_device_type collides with int... function signature ambiguous
	void initializeOpenCL();

public:
	//constructors

	//optionally specify device type and/or vendor using enum defined above.

	//~ OpenCLResource(cl_deviceType type = CL_DEVICE_TYPE_DEFAULT, cl_vendor vendor = VENDOR_ANY);
	OpenCLResource();					//cl_deviceType type = CL_DEVICE_TYPE_DEFAULT, cl_vendor vendor = VENDOR_ANY
	OpenCLResource(cl_deviceType type); //cl_vendor vendor = VENDOR_ANY
	OpenCLResource(cl_vendor vendor);   //cl_deviceType type = CL_DEVICE_TYPE_DEFAULT
	OpenCLResource(cl_deviceType type, cl_vendor vendor);

	//command line constructor, expects "--device gpu/cpu/accel" and/or "--vendor amd/intel/nvidia".  Defaults as above
	OpenCLResource(int argc, char **argv);
    //OpenCLResource(const std::vector<std::string> &);

	OpenCLResource(unsigned int platformID, unsigned int deviceID);				 //specify the platform and optionally device by integer ID
	OpenCLResource(unsigned int platformID, std::vector<unsigned int> deviceID); //specify the platform and optionally device by integer IDs. default uses all available devices on that platform.

    ~OpenCLResource() {}

	cl_int error; //use this for error checking in host program

	cl::Program getProgram() { return program; };								  //get this program, needed for creating kernel objects
	cl::Context getContext() { return context; };								  //get this context, needed for creating memory objects
	cl::CommandQueue getQueue(cl_uint deviceID = 0) { return queues[deviceID]; }; //get the command queue associated with device=deviceID from the list of devices available in the context

	bool getDoubleSupport(cl_uint deviceID = 0) { return platform_info.device_info[deviceID].doubleSupport; };
	cl_ulong getMaxMemAllocSize(cl_uint deviceID = 0) { return platform_info.device_info[deviceID].maxMemAllocSize; };
	std::string getDeviceCLVersion(cl_uint deviceID = 0) { return platform_info.device_info[deviceID].version; };
	cl_device_type getDeviceType(cl_uint deviceID = 0) { return platform_info.device_info[deviceID].devType; };

	void buildProgramFromString(std::string clProgramString, std::string buildOptions = "");
	void buildProgramFromSource(std::string filename, std::string buildOptions = "");

	//TODO: add support for binary/offline compilation etc - from openCLUtilities

	//prints the platform and device info related to this context
	void print();
};

//basic functions to scan opencl platforms and devices of the system and print the results
//TODO: query more/all platform and device properties
//TODO: switch for verbosity of printOpenCL routines: name only, basics, all
//TODO: other overloads for print opencl/platform/device? eg filters for vendor/type/...
std::vector<platformInfo> queryOpenCL();
platformInfo getPlatformInfo(cl::Platform platform, std::vector<cl::Device> devices = std::vector<cl::Device>());
platformInfo getPlatformInfo(cl::Platform platform, cl::Device device);
deviceInfo getDeviceInfo(cl::Device device);
void printOpenCL();
void printOpenCL(std::vector<platformInfo>);
void printPlatformInfo(platformInfo pi);
void printDeviceInfo(deviceInfo di);

//convert OpenCL error enum to human readable string
std::string CLErrorString(cl_int cl_error);

//read file contents into a string
std::string read_file(std::string filename);

#endif // OPENCL_RESOURCE_HPP_

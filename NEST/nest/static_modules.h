#ifndef STATIC_MODULES_H
#define STATIC_MODULES_H

// Add all in source modules:
#include "modelsmodule.h"
#include "precisemodule.h"
#include "topologymodule.h"

// Others
#include "interpret.h"

void add_static_modules( SLIInterpreter& engine )
{
  // Add all in source modules:
  engine.addmodule( new nest::ModelsModule() );
  engine.addmodule( new nest::PreciseModule() );
  engine.addmodule( new nest::TopologyModule() );
}

#endif

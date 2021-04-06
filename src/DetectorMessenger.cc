//
// ********************************************************************
// * License and Disclaimer                                           *
// *                                                                  *
// * The  Geant4 software  is  copyright of the Copyright Holders  of *
// * the Geant4 Collaboration.  It is provided  under  the terms  and *
// * conditions of the Geant4 Software License,  included in the file *
// * LICENSE and available at  http://cern.ch/geant4/license .  These *
// * include a list of copyright holders.                             *
// *                                                                  *
// * Neither the authors of this software system, nor their employing *
// * institutes,nor the agencies providing financial support for this *
// * work  make  any representation or  warranty, express or implied, *
// * regarding  this  software system or assume any liability for its *
// * use.  Please see the license in the file  LICENSE  and URL above *
// * for the full disclaimer and the limitation of liability.         *
// *                                                                  *
// * This  code  implementation is the result of  the  scientific and *
// * technical work of the GEANT4 collaboration.                      *
// * By using,  copying,  modifying or  distributing the software (or *
// * any work based  on the software)  you  agree  to acknowledge its *
// * use  in  resulting  scientific  publications,  and indicate your *
// * acceptance of all terms of the Geant4 Software license.          *
// ********************************************************************
//
// This is the modified version of the example electromagnetic/TestEm7/src/DetectorMessenger.cc
    
#include "DetectorMessenger.hh"
#include "DetectorConstruction.hh"
#include "G4UIdirectory.hh"
#include "G4UIcommand.hh"
#include "G4UIparameter.hh"
#include "G4UIcmdWithAString.hh"
#include "G4UIcmdWithAnInteger.hh"
#include "G4UIcmdWithADoubleAndUnit.hh"
#include "G4UIcmdWithoutParameter.hh"

DetectorMessenger::DetectorMessenger(DetectorConstruction * Det)
:G4UImessenger(),fDetector(Det),
 fTestemDir(0),
 fDetDir(0),    
 fSizeXCmd(0),
 fSizeYZCmd(0), 
 fLayerSizeYZCmd(0),
 fLayerNumberCmd(0),          
 fUpdateCmd(0)
{ 
  fTestemDir = new G4UIdirectory("/protonGB/");
  fTestemDir->SetGuidance(" detector control.");
  
  fDetDir = new G4UIdirectory("/protonGB/det/");
  fDetDir->SetGuidance("detector construction commands");
        
  fSizeXCmd = new G4UIcmdWithADoubleAndUnit("/protonGB/det/setSizeX",this);
  fSizeXCmd->SetGuidance("Set sizeX of the absorber");
  fSizeXCmd->SetParameterName("SizeX",false);
  fSizeXCmd->SetRange("SizeX>0.");
  fSizeXCmd->SetUnitCategory("Length");
  fSizeXCmd->AvailableForStates(G4State_PreInit,G4State_Idle);
  
  fSizeYZCmd = new G4UIcmdWithADoubleAndUnit("/protonGB/det/setSizeYZ",this);
  fSizeYZCmd->SetGuidance("Set sizeYZ of the absorber");
  fSizeYZCmd->SetParameterName("SizeYZ",false);
  fSizeYZCmd->SetRange("SizeYZ>0.");
  fSizeYZCmd->SetUnitCategory("Length");
  fSizeYZCmd->AvailableForStates(G4State_PreInit,G4State_Idle);
                
  fLayerSizeYZCmd = new G4UIcmdWithADoubleAndUnit("/protonGB/det/setSliceSizeYZ",this);
  fLayerSizeYZCmd->SetGuidance("Set LayersizeYZ of the absorber");
  fLayerSizeYZCmd->SetParameterName("LayerSizeYZ",false);
  fLayerSizeYZCmd->SetRange("LayerSizeYZ>0.");
  fLayerSizeYZCmd->SetUnitCategory("Length");
  fLayerSizeYZCmd->AvailableForStates(G4State_PreInit,G4State_Idle);

  fLayerNumberCmd = new G4UIcmdWithAnInteger("/protonGB/det/sliceNumber",this);
  fLayerNumberCmd->SetGuidance("Set number of fLayers.");
  fLayerNumberCmd->SetParameterName("layerNb",false);
  fLayerNumberCmd->SetRange("layerNb>=0");
  fLayerNumberCmd->AvailableForStates(G4State_PreInit,G4State_Idle);

  fUpdateCmd = new G4UIcmdWithoutParameter("/protonGB/det/update",this);
  fUpdateCmd->SetGuidance("Update calorimeter geometry.");
  fUpdateCmd->SetGuidance("This command MUST be applied before \"beamOn\" ");
  fUpdateCmd->SetGuidance("if you changed geometrical value(s).");
  fUpdateCmd->AvailableForStates(G4State_Idle);
}

DetectorMessenger::~DetectorMessenger()
{
  delete fSizeXCmd;
  delete fSizeYZCmd; 
  delete fLayerSizeYZCmd;
  delete fLayerNumberCmd;
  delete fUpdateCmd;
  delete fDetDir;  
  delete fTestemDir;
}

void DetectorMessenger::SetNewValue(G4UIcommand* command,G4String newValue)
{    
  if( command == fSizeXCmd )
   { fDetector->SetSizeX(fSizeXCmd->GetNewDoubleValue(newValue));}
   
  if( command == fSizeYZCmd )
   { fDetector->SetSizeYZ(fSizeYZCmd->GetNewDoubleValue(newValue));}

  if( command == fLayerSizeYZCmd )
   { fDetector->SetLayerSizeYZ(fLayerSizeYZCmd->GetNewDoubleValue(newValue));}

  if( command == fLayerNumberCmd )
   { fDetector->SetLayerNumber(fLayerNumberCmd->GetNewIntValue(newValue));}
    
  if( command == fUpdateCmd )
   { fDetector->UpdateGeometry();}
}



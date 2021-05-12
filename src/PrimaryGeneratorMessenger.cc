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
// This is the modified version of the example electromagnetic/TestEm7/src/PrimaryGeneratorMessenger.cc

#include "PrimaryGeneratorMessenger.hh"
#include "PrimaryGeneratorAction.hh"
#include "G4UIdirectory.hh"
#include "G4UIcmdWithADoubleAndUnit.hh"
#include "G4UIcmdWithAString.hh"

PrimaryGeneratorMessenger::PrimaryGeneratorMessenger(
                                                   PrimaryGeneratorAction* Gun)
:G4UImessenger(),fAction(Gun),
 fGunDir(0),         
 fRndmCmd(0),
 fPosX0Cmd(0),
 fPosY0Cmd(0),
 fPosZ0Cmd(0),
 fInputFileCmd(0)
{ 
  fGunDir = new G4UIdirectory("/protonPIC/gun/");
  fGunDir->SetGuidance("gun control");

  fRndmCmd = new G4UIcmdWithADoubleAndUnit("/protonPIC/gun/rndm",this);
  fRndmCmd->SetGuidance("random lateral extension on the beam");
  fRndmCmd->SetParameterName("rBeam",false);
  fRndmCmd->SetRange("rBeam>=0.");
  fRndmCmd->SetUnitCategory("Length");
  fRndmCmd->AvailableForStates(G4State_PreInit,G4State_Idle);  

  fPosX0Cmd = new G4UIcmdWithADoubleAndUnit("/protonPIC/gun/initPosX",this);
  fPosX0Cmd->SetGuidance("initial x0 position of the beam");
  fPosX0Cmd->SetParameterName("x0Beam",false);
  fPosX0Cmd->SetUnitCategory("Length");
  fPosX0Cmd->AvailableForStates(G4State_PreInit,G4State_Idle);  

  fPosY0Cmd = new G4UIcmdWithADoubleAndUnit("/protonPIC/gun/initPosY",this);
  fPosY0Cmd->SetGuidance("initial y0 position of the beam");
  fPosY0Cmd->SetParameterName("y0Beam",false);
  fPosY0Cmd->SetUnitCategory("Length");
  fPosY0Cmd->AvailableForStates(G4State_PreInit,G4State_Idle);  

  fPosZ0Cmd = new G4UIcmdWithADoubleAndUnit("/protonPIC/gun/initPosZ",this);
  fPosZ0Cmd->SetGuidance("initial z0 position of the beam");
  fPosZ0Cmd->SetParameterName("z0Beam",false);
  fPosZ0Cmd->SetUnitCategory("Length");
  fPosZ0Cmd->AvailableForStates(G4State_PreInit,G4State_Idle);  
  
  fInputFileCmd = new G4UIcmdWithAString("/protonPIC/gun/input",this);
  fInputFileCmd->SetGuidance("input root file for the beam");
  fInputFileCmd->SetParameterName("input",false);
}

PrimaryGeneratorMessenger::~PrimaryGeneratorMessenger()
{
  delete fInputFileCmd;
  delete fPosZ0Cmd;
  delete fPosY0Cmd;
  delete fPosX0Cmd;
  delete fRndmCmd;
  delete fGunDir;
}

void PrimaryGeneratorMessenger::SetNewValue(G4UIcommand* command,
                                               G4String newValue)
{ 
  if (command == fRndmCmd)
   {fAction->SetRndmBeam(fRndmCmd->GetNewDoubleValue(newValue));}   
  if (command == fPosX0Cmd)
   {fAction->SetInitPosXBeam(fPosX0Cmd->GetNewDoubleValue(newValue));}   
  if (command == fPosY0Cmd)
   {fAction->SetInitPosYBeam(fPosY0Cmd->GetNewDoubleValue(newValue));}   
  if (command == fPosZ0Cmd)
   {fAction->SetInitPosZBeam(fPosZ0Cmd->GetNewDoubleValue(newValue));}   
  if (command == fInputFileCmd)
   {fAction->SetInputFile(newValue);} 
}




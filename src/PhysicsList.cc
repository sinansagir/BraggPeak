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
// This is the modified version of the example electromagnetic/TestEm7/src/PhysicsList.cc
 
#include "PhysicsList.hh"
#include "PhysicsListMessenger.hh"
#include "G4ProcessManager.hh"
#include "G4Decay.hh"
#include "StepMax.hh"
#include "G4PhysicalConstants.hh"
#include "G4SystemOfUnits.hh"
#include "G4SystemOfUnits.hh"
#include "G4RunManager.hh"
#include "G4Region.hh"
#include "G4RegionStore.hh"
#include "G4PhysListFactory.hh"
#include "G4VPhysicsConstructor.hh"

// Physic lists (contained inside the Geant4 source code, 
// in the 'physicslists folder')
#include "G4HadronPhysicsQGSP_BIC.hh"
#include "G4EmStandardPhysics_option3.hh"
#include "G4EmLivermorePhysics.hh"
#include "G4EmPenelopePhysics.hh"
#include "G4EmExtraPhysics.hh"
#include "G4StoppingPhysics.hh"
#include "G4DecayPhysics.hh"
#include "G4HadronElasticPhysics.hh"
#include "G4HadronElasticPhysicsHP.hh"
#include "G4RadioactiveDecayPhysics.hh"
#include "G4IonBinaryCascadePhysics.hh"
#include "G4DecayPhysics.hh"
#include "G4NeutronTrackingCut.hh"
#include "G4LossTableManager.hh"
#include "G4UnitsTable.hh"
#include "G4ProcessManager.hh"
#include "G4IonFluctuations.hh"
#include "G4IonParametrisedLossModel.hh"
#include "G4EmProcessOptions.hh"
#include "G4ParallelWorldPhysics.hh"

PhysicsList::PhysicsList() : G4VModularPhysicsList(),
  fEmPhysicsList(0),
  fDecPhysicsList(0),
  fHadronPhys(),    
  fStepMaxProcess(0),
  fMessenger(0)
{
  G4LossTableManager::Instance();
  defaultCutValue = 1.*mm;
  fCutForGamma     = defaultCutValue;
  fCutForElectron  = defaultCutValue;
  fCutForPositron  = defaultCutValue;

  fStepMaxProcess  = 0;

  fMessenger = new PhysicsListMessenger(this);

  SetVerboseLevel(1);

  // Definition of some defaults for the physics     
  // in case no physics is called by the macro file  
  // EM physics
  fEmName = G4String("emstandard_opt3");  
  fEmPhysicsList = new G4EmStandardPhysics_option3(1);

  // Deacy physics and all particles
  fDecPhysicsList = new G4DecayPhysics();
  fraddecayList = new G4RadioactiveDecayPhysics();
}

PhysicsList::~PhysicsList()
{
  delete fMessenger;
  delete fEmPhysicsList;
  delete fDecPhysicsList;
  delete fraddecayList;
  for(size_t i=0; i<fHadronPhys.size(); i++) {delete fHadronPhys[i];}
}

void PhysicsList::ConstructParticle()
{
  fDecPhysicsList->ConstructParticle();
}

void PhysicsList::ConstructProcess()
{
  // transportation
  AddTransportation();
  
  // electromagnetic physics list
  fEmPhysicsList->ConstructProcess();

  // decay physics list
  fDecPhysicsList->ConstructProcess();
  fraddecayList->ConstructProcess();
  
  // hadronic physics lists
  for(size_t i=0; i<fHadronPhys.size(); i++) {
    fHadronPhys[i]->ConstructProcess();
  }
  
  // step limitation (as a full process)
  AddStepMax();  
}

void PhysicsList::AddPhysicsList(const G4String& name)
{
  if (verboseLevel>1) {
    G4cout << "PhysicsList::AddPhysicsList: <" << name << ">" << G4endl;
  }

  if (name == fEmName) return;

    if (name == "standard_opt3") {
    fEmName = name;
    delete fEmPhysicsList;
    fEmPhysicsList = new G4EmStandardPhysics_option3();
    G4RunManager::GetRunManager() -> PhysicsHasBeenModified();

  } else if (name == "emlivermore") {
    fEmName = name;
    delete fEmPhysicsList;
    fEmPhysicsList = new G4EmLivermorePhysics();
    G4RunManager::GetRunManager()-> PhysicsHasBeenModified();

  } else if (name == "empenelope") {
    fEmName = name;
    delete fEmPhysicsList;
    fEmPhysicsList = new G4EmPenelopePhysics();
    G4RunManager::GetRunManager()-> PhysicsHasBeenModified();
    
  } else if (name == "QGSP_BIC_EMY") {
    AddPhysicsList("emstandard_opt3");
    fHadronPhys.push_back( new G4HadronPhysicsQGSP_BIC());
    fHadronPhys.push_back( new G4EmExtraPhysics());
    fHadronPhys.push_back( new G4HadronElasticPhysics());
    fHadronPhys.push_back( new G4StoppingPhysics());
    fHadronPhys.push_back( new G4IonBinaryCascadePhysics());
    fHadronPhys.push_back( new G4NeutronTrackingCut());
    G4RunManager::GetRunManager()-> PhysicsHasBeenModified();
    
  } else { 
    G4cout << "PhysicsList::AddPhysicsList: <" << name << ">"
	   << " is not defined"
	   << G4endl;
  }
}

void PhysicsList::AddStepMax()
{
  // Step limitation seen as a process
  fStepMaxProcess = new StepMax();

  auto theParticleIterator=GetParticleIterator();
  theParticleIterator->reset();
  while ((*theParticleIterator)()){
    G4ParticleDefinition* particle = theParticleIterator->value();
    G4ProcessManager* pmanager = particle->GetProcessManager();

    if (fStepMaxProcess->IsApplicable(*particle) && pmanager)
      {
        pmanager ->AddDiscreteProcess(fStepMaxProcess);
      }
  }
}

void PhysicsList::SetCuts()
{
  if (verboseLevel >0) {
    G4cout << "PhysicsList::SetCuts:";
    G4cout << "CutLength : " << G4BestUnit(defaultCutValue,"Length") << G4endl;
  }

  // set cut values for gamma at first and for e- second and next for e+,
  // because some processes for e+/e- need cut values for gamma
  SetCutValue(fCutForGamma, "gamma");
  SetCutValue(fCutForElectron, "e-");
  SetCutValue(fCutForPositron, "e+");

  if (verboseLevel>0) DumpCutValuesTable();
}

void PhysicsList::SetCutForGamma(G4double cut)
{
  fCutForGamma = cut;
  SetParticleCuts(fCutForGamma, G4Gamma::Gamma());
}

void PhysicsList::SetCutForElectron(G4double cut)
{
  fCutForElectron = cut;
  SetParticleCuts(fCutForElectron, G4Electron::Electron());
}

void PhysicsList::SetCutForPositron(G4double cut)
{
  fCutForPositron = cut;
  SetParticleCuts(fCutForPositron, G4Positron::Positron());
}




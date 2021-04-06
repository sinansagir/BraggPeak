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
// This is the modified version of the example electromagnetic/TestEm7/src/StepMax.cc

#include "StepMax.hh"
#include "StepMaxMessenger.hh"

StepMax::StepMax(const G4String& processName)
 : G4VDiscreteProcess(processName),fMaxChargedStep(DBL_MAX),fMess(0)
{
  fMess = new StepMaxMessenger(this);
}

StepMax::~StepMax() { delete fMess; }

G4bool StepMax::IsApplicable(const G4ParticleDefinition& particle)
{
  return (particle.GetPDGCharge() != 0. && !particle.IsShortLived());
}

void StepMax::SetMaxStep(G4double step) {fMaxChargedStep = step;}

G4double StepMax::PostStepGetPhysicalInteractionLength( 
                                                 const G4Track& aTrack,
                                                       G4double,
                                                       G4ForceCondition* condition )
{
  // condition is set to "Not Forced"
  *condition = NotForced;
  
  G4double ProposedStep = DBL_MAX;

  if((fMaxChargedStep > 0.) &&
     (aTrack.GetVolume() != NULL) &&
     (aTrack.GetVolume()->GetName() != "World"))
     ProposedStep = fMaxChargedStep;

  return ProposedStep;
}

G4VParticleChange* StepMax::PostStepDoIt(const G4Track& aTrack, const G4Step&)
{
   // do nothing
   aParticleChange.Initialize(aTrack);
   return &aParticleChange;
}





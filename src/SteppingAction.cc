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
// This is the modified version of the example electromagnetic/TestEm7/src/SteppingAction.cc

#include "SteppingAction.hh"
#include "G4Step.hh"
#include "G4StepPoint.hh"
#include "DetectorConstruction.hh"
#include "RunAction.hh"
#include "Randomize.hh"

SteppingAction::SteppingAction(DetectorConstruction* det, RunAction* RuAct)
:G4UserSteppingAction(),fDetector(det), fRunAction(RuAct)
{ }

SteppingAction::~SteppingAction()
{ }

void SteppingAction::UserSteppingAction(const G4Step* step)
{
  G4double edep = step->GetTotalEnergyDeposit();
  if (edep <= 0.) return;
  
  fRunAction->FillEdep(edep);
  
  if (step->GetTrack()->GetTrackID() == 1) {
    fRunAction->AddPrimaryStep();
    /*
    G4cout << step->GetTrack()->GetMaterial()->GetName()
           << "  E1= " << step->GetPreStepPoint()->GetKineticEnergy()
           << "  E2= " << step->GetPostStepPoint()->GetKineticEnergy()
           << " Edep= " << edep << G4endl;
    */
  } 

  //Bragg curve
  G4StepPoint* prePoint  = step->GetPreStepPoint();
  G4StepPoint* postPoint = step->GetPostStepPoint();
   
  G4double x1 = prePoint->GetPosition().x();
  G4double x2 = postPoint->GetPosition().x();  
  G4double x  = x1 + G4UniformRand()*(x2-x1) + 0.5*(fDetector->GetAbsorSizeX());
  G4AnalysisManager* analysisManager = G4AnalysisManager::Instance();
  analysisManager->FillH1(1, x, edep); 
  analysisManager->FillH1(2, x, edep);
  
  //fill layers
  G4int copyNb = prePoint->GetTouchableHandle()->GetCopyNumber();
  if (copyNb > 0) fRunAction->FillLayerEdep(copyNb, edep); 
}





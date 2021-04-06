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
// This is the modified version of the example electromagnetic/TestEm7/include/RunAction.hh
   
#ifndef RunAction_h
#define RunAction_h 1

#include "G4UserRunAction.hh"
#include "globals.hh"
#include "g4root.hh"
//#include "g4xml.hh"

class DetectorConstruction;
class PhysicsList;
class PrimaryGeneratorAction;
class G4Run;

class RunAction : public G4UserRunAction
{
public:

  RunAction(DetectorConstruction*, PhysicsList*, PrimaryGeneratorAction*);
 ~RunAction();

  virtual void   BeginOfRunAction(const G4Run*);
  virtual void   EndOfRunAction(const G4Run*);
    
  inline void FillLayerEdep(G4int n, G4double e);
  inline void FillEdep(G4double de);
  inline void AddPrimaryStep();
                   
private:  
    
  void BookHisto();

  G4AnalysisManager*      fAnalysisManager;
  DetectorConstruction*   fDetector;
  PhysicsList*            fPhysics;
  PrimaryGeneratorAction* fKinematic;   
  G4double*               fLayerEdep;
  G4double                fEdeptot;
  G4int                   fNbPrimarySteps;
};
  
inline void RunAction::FillLayerEdep(G4int n, G4double e)  
{
  fLayerEdep[n] += e;
}

inline void RunAction::FillEdep(G4double de) 
{
  fEdeptot += de; 
}
    
inline void RunAction::AddPrimaryStep() 
{
  ++fNbPrimarySteps;
}
                   
#endif


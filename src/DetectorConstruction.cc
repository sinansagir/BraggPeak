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
// This is the modified version of the example electromagnetic/TestEm7/src/DetectorConstruction.cc


#include "DetectorConstruction.hh"
#include "DetectorMessenger.hh"

#include "G4Material.hh"
#include "G4Box.hh"
#include "G4LogicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4UniformMagField.hh"
#include "G4PVReplica.hh"

#include "G4GeometryManager.hh"
#include "G4PhysicalVolumeStore.hh"
#include "G4LogicalVolumeStore.hh"
#include "G4SolidStore.hh"

#include "G4NistManager.hh"
#include "G4UnitsTable.hh"

#include "G4TransportationManager.hh"
#include "G4RunManager.hh" 

#include "G4PhysicalConstants.hh"
#include "G4SystemOfUnits.hh"

DetectorConstruction::DetectorConstruction()
: G4VUserDetectorConstruction(),
  fWorldMaterial(0),fAbsorMaterial(0),fLAbsor(0),
  fDetectorMessenger(0)
{
  // default parameter values
  fAbsorSizeX = fAbsorSizeYZ = 20*cm;
  fWorldSizeX = fWorldSizeYZ = 1.2*fAbsorSizeX;

  fLayerSizeYZ = 2*cm;
  fLayerNumber = 0;
  fLayerSizeX = 0*cm;
  fLayerMass = 0;
  
  fWorldMaterial = fAbsorMaterial = 0;
  fLAbsor   = 0;
      
  DefineMaterials();
  
  // create commands for interactive definition of the detector  
  fDetectorMessenger = new DetectorMessenger(this);
}


DetectorConstruction::~DetectorConstruction()
{ delete fDetectorMessenger;}


G4VPhysicalVolume* DetectorConstruction::Construct()
{
  return ConstructVolumes();
}


void DetectorConstruction::DefineMaterials()
{ 
  // define Elements
  G4double z, a;

  G4Element* H = new G4Element("Hydrogen", "H", z= 1, a= 1.008*g/mole);
  G4Element* O = new G4Element("Oxygen"  , "O", z= 8, a= 16.00*g/mole);

  // define Materials
  G4double density, temperature, pressure;
  G4int    natoms, ncomponents;
 
  G4Material* H2O = 
    new G4Material("Water", density= 1.0*g/cm3, ncomponents=2);
  H2O->AddElement(H, natoms=2);
  H2O->AddElement(O, natoms=1);
  H2O->GetIonisation()->SetMeanExcitationEnergy(78.0*eV);

  density     = universe_mean_density;    //from PhysicalConstants.h
  pressure    = 3.e-18*pascal;
  temperature = 2.73*kelvin;
  G4Material* vacuum = 
    new G4Material("Galactic",z= 1,a= 1.008*g/mole,density,
                   kStateGas,temperature,pressure);

  //default materials
  fWorldMaterial = vacuum;
  fAbsorMaterial = H2O;
}

  
G4VPhysicalVolume* DetectorConstruction::ConstructVolumes()
{
  G4GeometryManager::GetInstance()->OpenGeometry();
  G4PhysicalVolumeStore::GetInstance()->Clean();
  G4LogicalVolumeStore::GetInstance()->Clean();
  G4SolidStore::GetInstance()->Clean();

  // World
  G4Box*
  sWorld = new G4Box("World",                                      
                   fWorldSizeX/2,fWorldSizeYZ/2,fWorldSizeYZ/2);   

  G4LogicalVolume*
  lWorld = new G4LogicalVolume(sWorld,                        
                               fWorldMaterial,                
                              "World");                       

  G4VPhysicalVolume*                                   
  pWorld = new G4PVPlacement(0,                           
                             G4ThreeVector(),             
                             lWorld,                      
                             "World",                     
                             0,                           
                             false,                       
                             0);                          
                            
  // Absorber                           
  G4Box*
  sAbsor = new G4Box("Absorber",                                 
                   fAbsorSizeX/2,fAbsorSizeYZ/2,fAbsorSizeYZ/2); 
                                                                 
  fLAbsor = new G4LogicalVolume(sAbsor,                   
                               fAbsorMaterial,            
                              "Absorber");                
  
                              
           new G4PVPlacement(0,                          
                             G4ThreeVector(),            
                            fLAbsor,                     
                            "Absorber",                  
                            lWorld,                      
                            false,                       
                            0);                          

   // Layer
   if (fLayerNumber > 0) {
      fLayerSizeX = fAbsorSizeX/fLayerNumber;
      G4Box* sLayer = new G4Box("Layer", fLayerSizeX/2,fLayerSizeYZ/2,fLayerSizeYZ/2); 
      fLLayer = new G4LogicalVolume(sLayer, fAbsorMaterial, "Layer");	
      fPhysLayer = new G4PVReplica("Layer",		
      		                    fLLayer,		
      	                            fLAbsor,		
                                    kXAxis,		
                                    fLayerNumber,		
                                    fLayerSizeX);	

      fLayerMass = fLayerSizeX*fLayerSizeYZ*fLayerSizeYZ*(fAbsorMaterial->GetDensity());

    }                


  PrintParameters();
    
  //always return the World volume 
  return pWorld;
}

void DetectorConstruction::PrintParameters()
{
  G4cout << *(G4Material::GetMaterialTable()) << G4endl;
  G4cout << "\n---------------------------------------------------------\n";
  G4cout << "---> The Absorber is " << G4BestUnit(fAbsorSizeX,"Length")
         << " of " << fAbsorMaterial->GetName() << G4endl;
  G4cout << "\n---------------------------------------------------------\n";
  
}

void DetectorConstruction::SetSizeX(G4double value)
{
  fAbsorSizeX = value; fWorldSizeX = 1.2*fAbsorSizeX;
  G4RunManager::GetRunManager()->GeometryHasBeenModified();
}
  
void DetectorConstruction::SetSizeYZ(G4double value)
{
  fAbsorSizeYZ = value; 
  fWorldSizeYZ = 1.2*fAbsorSizeYZ;
  G4RunManager::GetRunManager()->GeometryHasBeenModified();
}  

void DetectorConstruction::SetLayerSizeYZ(G4double value)
{
  fLayerSizeYZ = value; 
  G4RunManager::GetRunManager()->GeometryHasBeenModified();
}  

void DetectorConstruction::SetLayerNumber(G4int value)
{
  fLayerNumber = value; 
  G4RunManager::GetRunManager()->GeometryHasBeenModified();
}    
  
void DetectorConstruction::UpdateGeometry()
{
  G4RunManager::GetRunManager()->PhysicsHasBeenModified();
  G4RunManager::GetRunManager()->DefineWorldVolume(ConstructVolumes());
}



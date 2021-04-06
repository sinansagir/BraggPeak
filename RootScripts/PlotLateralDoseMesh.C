{  
#include <vector>

    // Read simulation file       
    //change this line if you modify the length and width of the box
    Float_t lengthBox = 40, widthBox = 40; 
    
    TString doseFileSim = "DoseLateralMesh_Mod.txt";
    TNtuple *TNtupleSim = new TNtuple("ntupleSimulation","dose from simulation file", "iX:jY:kZ:doseSim");

    cout << "Reading file \" " << doseFileSim << "\" ... ";
    Long64_t nlines = TNtupleSim -> ReadFile(doseFileSim, "iX:jY:kZ:doseSim"); 
    if (nlines <=0){cout << "Error: Check file \"" << doseFileSim << "\"\n"; return;}
    printf("%d Experimental points found\n", nlines);
        
    Float_t kZ, doseSim;
    TNtupleSim -> SetBranchAddress("kZ", &kZ);
    TNtupleSim -> SetBranchAddress("doseSim", &doseSim);

    // Normalise and fill TNtupleSim
    Int_t nentries = (Int_t)TNtupleSim -> GetEntries();   
    TNtupleSim -> GetEntry(0);
    Float_t maxDose = 0, depthSim = 0, slength = widthBox/nentries;
    vector <Float_t> vec_dose, vec_kZ;

    for (Int_t l = 0; l<nentries; l++)
    {
      TNtupleSim -> GetEntry(l);
      if (maxDose < doseSim) { maxDose = doseSim;
                               vec_dose.push_back(doseSim);
                               vec_kZ.push_back(depthSim);                             
                              }
      else { vec_dose.push_back(doseSim);
             vec_kZ.push_back(depthSim);

            }
      depthSim += slength;
    }
    
    TNtupleSim -> Reset(); 

    // normalisation to the maximum dose
    for (Int_t l = 0; l<vec_dose.size();l++)
    {
        kZ = vec_kZ[l];
	doseSim = 100*(vec_dose[l]/maxDose);
        TNtupleSim -> Fill(0,0,kZ,doseSim);
    }
      
    TCanvas *c1 = new TCanvas ("c1","c1",200,10,600,400);
     
    TNtupleSim-> SetMarkerStyle(20);
    TNtupleSim -> SetMarkerColor(4);
    TNtupleSim -> SetMarkerSize(0.7);
       
    TNtupleSim ->  Draw("doseSim:kZ");
    TH2F *htemp = (TH2F*)gPad->GetPrimitive("htemp");
    TAxis *xaxis = htemp->GetXaxis();
    TAxis *yaxis = htemp->GetYaxis();
    xaxis->SetTitle("Width [mm]");
    yaxis->SetTitle("Dose [%]");
    htemp -> SetTitle("Lateral dose");
    
    // Legend
    leg = new TLegend(0.50,0.60,0.20,0.70); 
    leg -> SetTextSize(0.04);
    leg -> SetFillColor(0);
    leg -> AddEntry(TNtupleSim, "Geant4, lateral dose", "P");
    leg -> Draw();

    //c1->SaveAs("BraggPeakComparison_Mesh.png");
    c1->SaveAs("LateralDose_Mesh.root");  
}

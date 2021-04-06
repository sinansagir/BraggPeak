{  
#include <vector>
    gROOT->Reset();
    TFile * file = new TFile("BraggPeakComparison_Mesh.root","RECREATE");
   
    // Read experimental data file
    TString doseFileExp = "ClatterbridgeData.txt";
    TNtuple *ntupleExperimental = new TNtuple("ntupleExperimental","dose from exp. data", "depthExp:doseExp");

    cout << "Reading file \" " << doseFileExp << "\" ... ";
    Long64_t nlines = ntupleExperimental -> ReadFile(doseFileExp, "depthExp:doseExp"); 
    if (nlines <=0){cout << "Error: Check file \"" << doseFileExp << "\"\n"; return;}
    printf("%d Experimental points found\n", nlines); 

    // Read simulation file       
    //change this line if you modify the length and width of the box
    Float_t lengthBox = 40, widthBox = 40; 
    
    TString doseFileSim = "DoseLongitudinalMesh_Mod.txt";
    TNtuple *TNtupleSim = new TNtuple("ntupleSimulation","dose from simulation file", "iX:jY:kZ:doseSim");

    cout << "Reading file \" " << doseFileSim << "\" ... ";
    Long64_t nlines = TNtupleSim -> ReadFile(doseFileSim, "iX:jY:kZ:doseSim"); 
    if (nlines <=0){cout << "Error: Check file \"" << doseFileSim << "\"\n"; return;}
    printf("%d Experimental points found\n", nlines);
        
    Float_t iX, doseSim;
    TNtupleSim -> SetBranchAddress("iX", &iX);
    TNtupleSim -> SetBranchAddress("doseSim", &doseSim);

    // Normalise and fill TNtupleSim
    Int_t nentries = (Int_t)TNtupleSim -> GetEntries();   
    TNtupleSim -> GetEntry(0);
    Float_t maxDose = 0, depthSim = 0, slength = lengthBox/nentries;
    vector <Float_t> vec_dose, vec_iX;

    for (Int_t l = 0; l<nentries; l++)
    {
      TNtupleSim -> GetEntry(l);
      if (maxDose < doseSim) { maxDose = doseSim;
                               vec_dose.push_back(doseSim);
                               vec_iX.push_back(depthSim);                             
                              }
      else { vec_dose.push_back(doseSim);
             vec_iX.push_back(depthSim);

            }
      depthSim += slength;
    }
    
    TNtupleSim -> Reset(); 

    // normalisation to the maximum dose
    for (Int_t l = 0; l<vec_dose.size();l++)
    {
        iX = vec_iX[l];
	doseSim = 100*(vec_dose[l]/maxDose);
        TNtupleSim -> Fill(iX,0,0,doseSim);
    }
    
  
    TCanvas *c1 = new TCanvas ("c1","c1",200,10,600,400);
     
    TNtupleSim-> SetMarkerStyle(20);
    TNtupleSim -> SetMarkerColor(4);
    TNtupleSim -> SetMarkerSize(0.7);
    
    ntupleExperimental -> SetMarkerStyle(20);
    ntupleExperimental -> SetMarkerColor(2);
    ntupleExperimental -> SetMarkerSize(0.4);
   
    ntupleExperimental  -> Draw("doseExp:depthExp");
    TNtupleSim ->  Draw("doseSim:iX","","same");
    TH2F *htemp = (TH2F*)gPad->GetPrimitive("htemp");
    TAxis *xaxis = htemp->GetXaxis();
    TAxis *yaxis = htemp->GetYaxis();
    xaxis->SetTitle("Depth [mm]");
    yaxis->SetTitle("Dose [%]");
    htemp -> SetTitle("Bragg peak");
    
    // Legend
    leg = new TLegend(0.50,0.60,0.20,0.70); 
    leg -> SetTextSize(0.04);
    leg -> SetFillColor(0);
    leg -> AddEntry(ntupleExperimental, "Clatterbridge", "P");
    leg -> AddEntry(TNtupleSim, "Geant4, scoring mesh", "P");
    leg -> Draw();

    //c1->SaveAs("BraggPeakComparison_Mesh.png");
    c1->SaveAs("BraggPeakComparison_Mesh.root");  
}

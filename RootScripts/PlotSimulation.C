{  
#include <vector>
    gROOT->Reset();
    TFile * file = new TFile("Simulation.root","RECREATE");

    // Load experimental data file
    TString doseFileSim = "PlotDose.txt";
    TNtuple *ntupleSimulation = new TNtuple("ntupleSimulation","dose from simulation", "depthSim:doseSim");

    vector <Float_t> vec_dose, vec_iX;
    cout << "Reading file \" " << doseFileSim << "\" ... ";
    Long64_t nlines = ntupleSimulation -> ReadFile(doseFileSim, "depthSim:doseSim"); 
    if (nlines <=0){cout << "Error: Check file \"" << doseFileSim << "\"\n"; return;}
    printf("%d Simulation points found\n", nlines); 
    
    TCanvas *c1 = new TCanvas ("c1","c1",200,10,600,400);
         
    ntupleSimulation -> SetMarkerStyle(20);
    ntupleSimulation -> SetMarkerColor(4);
    ntupleSimulation -> SetMarkerSize(0.7);
   
    ntupleSimulation -> Draw("doseSim:depthSim");
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
    leg -> AddEntry(ntupleSimulation, "Geant4", "P");
    leg -> Draw();
  
    //c1->SaveAs("Simulation.png");
    c1->SaveAs("Simulation.root");

}

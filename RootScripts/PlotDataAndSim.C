{  
#include <vector>
    gROOT->Reset();
    TFile * file = new TFile("BraggPeakComparison.root","RECREATE");

    // Load experimental data file
    TString doseFileExp = "ClatterbridgeData.txt";
    TNtuple *ntupleExperimental = new TNtuple("ntupleExperimental","dose from exp data", "depthExp:doseExp");

    vector <Float_t> vec_dose, vec_iX;
    cout << "Reading file \" " << doseFileExp << "\" ... ";
    Long64_t nlines = ntupleExperimental -> ReadFile(doseFileExp, "depthExp:doseExp"); 
    if (nlines <=0){cout << "Error: Check file \"" << doseFileExp << "\"\n"; return;}
    printf("%d Experimental points found\n", nlines); 
    
    // Load simulation file  
    TString doseFileSim = "PlotDose.txt"; 
    TNtuple *TNtupleSim = new TNtuple("ntupleSimulation","dose from sim file", "depthSim:doseSim"); 
       
    cout << "Reading file \" " << doseFileExp << "\" ... ";
    Long64_t nlines = TNtupleSim -> ReadFile(doseFileSim, "depthSim:doseSim"); 
    if (nlines <=0){cout << "Error: Check file \"" << doseFileExp << "\"\n"; return;}    
    printf("%d Simulated points found\n", nlines); 

    TCanvas *c1 = new TCanvas ("c1","c1",200,10,600,400);
     
    TNtupleSim-> SetMarkerStyle(20);
    TNtupleSim -> SetMarkerColor(4);
    TNtupleSim -> SetMarkerSize(0.7);
    
    ntupleExperimental -> SetMarkerStyle(20);
    ntupleExperimental -> SetMarkerColor(2);
    ntupleExperimental -> SetMarkerSize(0.4);
   
    ntupleExperimental  -> Draw("doseExp:depthExp");
    TNtupleSim ->  Draw("doseSim:depthSim","","same");
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
    leg -> AddEntry(TNtupleSim, "Geant4", "P");
    leg -> Draw();

    //c1->SaveAs("BraggPeakComparison.png");
    c1->SaveAs("BraggPeakComparison.root");
}

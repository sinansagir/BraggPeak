{  
#include <vector>
    gROOT->Reset();
    TFile * file = new TFile("ClatterbridgeData.root","RECREATE");

    // Load experimental data file
    TString doseFileExp = "ClatterbridgeData.txt";
    TNtuple *ntupleExperimental = new TNtuple("ntupleExperimental","dose from exp data", "depthExp:doseExp");

    vector <Float_t> vec_dose, vec_iX;
    cout << "Reading file \" " << doseFileExp << "\" ... ";
    Long64_t nlines = ntupleExperimental -> ReadFile(doseFileExp, "depthExp:doseExp"); 
    if (nlines <=0){cout << "Error: Check file \"" << doseFileExp << "\"\n"; return;}
    printf("%d Experimental points found\n", nlines); 
    
    TCanvas *c1 = new TCanvas ("c1","c1",200,10,600,400);
         
    ntupleExperimental -> SetMarkerStyle(20);
    ntupleExperimental -> SetMarkerColor(2);
    ntupleExperimental -> SetMarkerSize(0.4);
   
    ntupleExperimental -> Draw("doseExp:depthExp");
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
    leg -> Draw();
  
    //c1->SaveAs("ClatterbridgeData.png");
    c1->SaveAs("ClatterbridgeData.root");

}

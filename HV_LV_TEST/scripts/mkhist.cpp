void mkhist(){

    std::vector<std::vector<int>> v_bins;
    std::vector<int> v_cols;
    std::vector<std::string> v_titles;
    std::vector<TH1D> v_hist;

    // R_{VIN}
    std::vector<int> v_bin_vin = {28, 0, 14};
    int col_vin = kAzure+1;
    std::string title_vin = "PowerRail Resistance";
    v_bins.push_back(v_bin_vin);
    v_cols.push_back(col_vin);
    v_titles.push_back(title_vin);

    // R_{GND}
    std::vector<int> v_bin_gnd = {28, 0, 14};
    int col_gnd = kGreen+3;
    std::string title_gnd = "GroundRail Resistance";
    v_bins.push_back(v_bin_gnd);
    v_cols.push_back(col_gnd);
    v_titles.push_back(title_gnd);

    // R_{eff}
    std::vector<int> v_bin_eff = {32, 0, 16};
    int col_eff = kRed+1;
    std::string title_eff = "Effective Resistance";
    v_bins.push_back(v_bin_eff);
    v_cols.push_back(col_eff);
    v_titles.push_back(title_eff);

    // Leakage Current
    std::vector<int> v_bin_cur = {20, 0, 10};
    int col_cur = kOrange+1;
    std::string title_cur = "Leakage Current";
    v_bins.push_back(v_bin_cur);
    v_cols.push_back(col_cur);
    v_titles.push_back(title_cur);

    TCanvas *c1 = new TCanvas("c1", "Split Canvas with Details", 1000, 1000);
    c1->Divide(2, 2);

    for(int i=0; i<v_bins.size(); i++){
        c1 -> cd(i+1);

        //common Info
        std::ifstream ifs("../data/results/HV_LV_TEST.txt");
        if(!ifs){std::cout << "Can NOT open HV LV TEST Info List..." << std::endl;}
        std::string line;
        std::getline(ifs, line);
        std::string i_serialNum;
        double i_Rvin, i_Rgnd, i_Reff, i_cur;
        double target;

        int total_bin = v_bins[i][0];
        int min_bin = v_bins[i][1];
        int max_bin = v_bins[i][2];

        double offset = (max_bin-min_bin)/(total_bin*2);
        TH1D* hist1 = new TH1D(Form("hist1_%d", i), "hist1", total_bin, min_bin+offset, max_bin+offset);

         while(ifs >> i_serialNum >> i_Rvin >> i_Rgnd >> i_Reff >> i_cur){

            if(v_titles[i]=="PowerRail Resistance"){target=i_Rvin;}
            else if(v_titles[i]=="GroundRail Resistance"){target=i_Rgnd;}
            else if(v_titles[i]=="Effective Resistance"){target=i_Reff;}
            else if(v_titles[i]=="Leakage Current"){target=i_cur;}

            if(target<v_bins[i][1]){hist1->Fill(v_bins[i][1]);}
            else if(target>v_bins[i][2]){hist1->Fill(v_bins[i][2]);}
            else{hist1->Fill(target);}
         }

         gPad->SetLogy(1);

        hist1 -> SetTitle(v_titles[i].c_str());
        hist1 -> GetYaxis() -> SetTitle("# of Flex");
        hist1 -> GetXaxis() -> SetTitleSize(0.04); 
        hist1 -> GetYaxis() -> SetTitleSize(0.04);
        hist1 -> SetLineColor(v_cols[i]);
        hist1 -> SetLineWidth(3);
        hist1 -> SetStats(0);
        hist1 -> Draw();

        if(v_titles[i]=="Leakage Current"){hist1 -> GetXaxis() -> SetTitle("Leakage Current [nA]");}
        else{
            hist1 -> GetXaxis() -> SetTitle("Thickness [um]");
            TLine* line1 = new TLine(12, hist1->GetMinimum(), 12, hist1->GetMaximum());
            line1 -> SetLineColor(kRed);
            line1 -> SetLineStyle(2);
            line1 -> SetLineWidth(4);
            line1 -> Draw("same");
        }
    }
    c1->Update();
    c1->SaveAs("../data/img/HV_LV_TEST.pdf");
}


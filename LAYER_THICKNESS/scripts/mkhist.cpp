void mkhist(){

    double ENING = 4.5;

    //vector to store Info about each Thickness
    std::vector<std::vector<int>> v_bins;
    std::vector<int> v_cols;
    std::vector<std::string> v_titles;
    std::vector<std::vector<double>> v_cri;
    std::vector<int> v_cri_col;
    std::vector<TH1D> v_hist;

    //1 : All Thickness
    std::vector<int> v_bin_all = {110, 180, 290};
    int col_all = kOrange+1;
    std::string title_all = "All Thickness";
    std::vector<double> v_cri_all = {188.8, 283.2};
    int cri_col_all = kRed;
    v_bins.push_back(v_bin_all);
    v_cols.push_back(col_all);
    v_titles.push_back(title_all);
    v_cri.push_back(v_cri_all);
    v_cri_col.push_back(cri_col_all);

    //2 : Dielectric
    std::vector<int> v_bin_die = {30, 70, 100};
    int col_die = kGreen-8;
    std::string title_die = "Dielectric";
    std::vector<double> v_cri_die = {10.0, 30.0};
    int cri_col_die = kGray+2;
    v_bins.push_back(v_bin_die);
    v_cols.push_back(col_die);
    v_titles.push_back(title_die);
    v_cri.push_back(v_cri_die);
    v_cri_col.push_back(cri_col_die);

    //3 : Coverlay
    std::vector<int> v_bin_cov = {80, 40, 120}; 
    int col_cov = kAzure-8;
    std::string title_cov = "Coverlay";
    std::vector<double> v_cri_cov = {55.0, 70.0};
    int cri_col_cov = kGray+2;
    v_bins.push_back(v_bin_cov);
    v_cols.push_back(col_cov);
    v_titles.push_back(title_cov);
    v_cri.push_back(v_cri_cov);
    v_cri_col.push_back(cri_col_cov);

    //4 : Top Thickness
    std::vector<int> v_bin_top = {50, 20, 45};
    int col_top = kRed;
    std::string title_top = "Top Thickness";
    std::vector<double> v_cri_top = {20.0+ENING, 35.0+ENING};
    int cri_col_top = kRed;
    v_bins.push_back(v_bin_top);
    v_cols.push_back(col_top);
    v_titles.push_back(title_top);
    v_cri.push_back(v_cri_top);
    v_cri_col.push_back(cri_col_top);

    //5 : Inner Thickness
    std::vector<int> v_bin_inn = {26, 5, 18};
    int col_inn = kGreen;
    std::string title_inn = "Inner Thickness";
    std::vector<double> v_cri_inn = {9.0, 13.5};
    int cri_col_inn = kRed;
    v_bins.push_back(v_bin_inn);
    v_cols.push_back(col_inn);
    v_titles.push_back(title_inn);
    v_cri.push_back(v_cri_inn);
    v_cri_col.push_back(cri_col_inn);

    //6 : Bottom Thickness
    std::vector<int> v_bin_bot = {44, 22, 44};
    int col_bot = kBlue;
    std::string title_bot = "Bottom Thickness";
    std::vector<double> v_cri_bot = {20.0+ENING, 35.0+ENING};
    int cri_col_bot = kRed;
    v_bins.push_back(v_bin_bot);
    v_cols.push_back(col_bot);
    v_titles.push_back(title_bot);
    v_cri.push_back(v_cri_bot);
    v_cri_col.push_back(cri_col_bot);

    TCanvas *c1 = new TCanvas("c1", "Split Canvas with Details", 1200, 800);
    c1->Divide(3, 2);

    for(int i=0; i<v_bins.size(); i++){
        c1 -> cd(i+1);

        //common Info
        std::ifstream ifs("../data/results/LayerThickness.txt");
        if(!ifs){std::cout << "Can NOT open Layer Thickness Info List..." << std::endl;}
        std::string line;
        std::getline(ifs, line);
        std::string serialNum, islatest;
        double i_bot, i_cov, i_die, i_inn, i_sol, i_all, i_top, i_cup, i_time;
        double target;

        int total_bin = v_bins[i][0];
        int min_bin = v_bins[i][1];
        int max_bin = v_bins[i][2];

        double offset = (max_bin-min_bin)/(total_bin*2);

        TH1D* hist1 = new TH1D(Form("hist1_%d", i), "hist1", total_bin, min_bin+offset, max_bin+offset);
        //TH1D* hist2 = new TH1D("hist2", "hist2", total_bin, min_bin+offset, max_bin+offset);

        while(ifs >> serialNum >> i_bot >> i_cov >> i_die >> i_inn >> i_all >> i_top){

            if(v_titles[i]=="All Thickness"){target=i_all;}
            else if(v_titles[i]=="Dielectric"){target=i_die;}
            else if(v_titles[i]=="Coverlay"){target=i_cov;}
            else if(v_titles[i]=="Top Thickness"){target=i_top;}
            else if(v_titles[i]=="Inner Thickness"){target=i_inn;}
            else if(v_titles[i]=="Bottom Thickness"){target=i_bot;}
            else{std::cout << "strange Info.." << std::endl;}

            if(target<v_bins[i][1]){hist1->Fill(v_bins[i][1]);}
            else if(target>v_bins[i][2]){hist1->Fill(v_bins[i][2]);}
            else{hist1->Fill(target);}

        }
        
        gPad->SetLogy(1);

        hist1 -> SetTitle(v_titles[i].c_str());
        hist1 -> GetXaxis() -> SetTitle("Thickness [um]");
        hist1 -> GetYaxis() -> SetTitle("# of Flex");
        hist1 -> GetXaxis() -> SetTitleSize(0.04); 
        hist1 -> GetYaxis() -> SetTitleSize(0.04);
        hist1 -> SetLineColor(v_cols[i]);
        hist1 -> SetLineWidth(3);
        hist1 -> SetStats(0);
        hist1 -> Draw();

        TLine* line1 = new TLine(v_cri[i][0], hist1->GetMinimum(), v_cri[i][0], hist1->GetMaximum());
        line1 -> SetLineColor(v_cri_col[i]);
        line1 -> SetLineStyle(2);
        line1 -> SetLineWidth(4);
        line1 -> Draw("same");

        TLine* line2 = new TLine(v_cri[i][1], hist1->GetMinimum(), v_cri[i][1], hist1->GetMaximum());
        line2 -> SetLineColor(v_cri_col[i]);
        line2 -> SetLineStyle(2);
        line2 -> SetLineWidth(4);
        line2 -> Draw("same");

    }
    c1->Update();
    c1->SaveAs("../data/img/LayerThickness.pdf");
    
}     
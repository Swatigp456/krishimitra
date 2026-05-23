# populate_schemes.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'krishimitra.settings')
django.setup()

from schemes.models import GovernmentScheme

def populate_schemes():
    """Populate all Government of India schemes for farmers"""
    
    schemes_data = [
        # Income Support Schemes
        {
            'name': 'Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)',
            'name_hi': 'प्रधानमंत्री किसान सम्मान निधि',
            'short_description': 'Direct income support of ₹6,000 per year to small and marginal farmers',
            'description': 'PM-KISAN is a central sector scheme launched in February 2019 to supplement the financial needs of land-holding farmers. Under the scheme, a financial benefit of ₹6,000/- per year is transferred in three equal installments, into the Aadhaar seeded bank accounts of farmers through Direct Benefit Transfer (DBT) mode.',
            'benefits': '₹6,000 per year in three equal installments of ₹2,000 each. Over ₹3.69 lakh crore disbursed to farmers since inception.',
            'eligibility': 'All land-holding farmers with cultivable land. Exclusions apply for those with higher economic status (income tax payers, government employees, etc.)',
            'application_process': 'Apply online through PM-KISAN portal or visit nearest Common Service Centre (CSC). Aadhaar and land records required.',
            'documents_required': 'Aadhaar Card, Land Records, Bank Account Details',
            'category': 'income_support',
            'financial_assistance': '₹6,000 per year',
            'website': 'https://pmkisan.gov.in',
            'icon': '💰'
        },
        {
            'name': 'Pradhan Mantri Kisan Maan Dhan Yojana (PM-KMY)',
            'name_hi': 'प्रधानमंत्री किसान मानधन योजना',
            'short_description': 'Pension scheme for small and marginal farmers after 60 years of age',
            'description': 'PM-KMY is a pension scheme for small and marginal farmers providing ₹3,000 monthly pension after attaining 60 years of age.',
            'benefits': 'Monthly pension of ₹3,000 after 60 years of age. Family gets 50% pension after farmer\'s death.',
            'eligibility': 'Small and marginal farmers (land holding up to 2 hectares) between 18-40 years of age',
            'application_process': 'Apply online through PM-KMY portal or CSC. Monthly contribution between ₹55-200 based on entry age.',
            'documents_required': 'Aadhaar Card, Land Records, Bank Account Details, Age Proof',
            'category': 'pension',
            'financial_assistance': '₹3,000 monthly pension',
            'website': 'https://maandhan.in',
            'icon': '👴'
        },
        
        # Crop Insurance Schemes
        {
            'name': 'Pradhan Mantri Fasal Bima Yojana (PMFBY)',
            'name_hi': 'प्रधानमंत्री फसल बीमा योजना',
            'short_description': 'Comprehensive crop insurance against natural calamities, pests, and diseases',
            'description': 'PMFBY provides financial support to farmers suffering crop loss/damage arising out of natural calamities, adverse weather incidence. Farmers pay only 1.5-2% premium for Kharif/Rabi crops.',
            'benefits': 'Claims of over ₹1.83 lakh crore paid to farmers (5 times the premium paid). Covers pre-sowing to post-harvest losses.',
            'eligibility': 'All farmers growing notified crops in notified areas. Scheme is voluntary for farmers.',
            'application_process': 'Apply through bank/PACs/CSC before sowing season. Premium payment along with loan application.',
            'documents_required': 'Land Records, Bank Account Details, Crop Sowing Declaration',
            'category': 'insurance',
            'financial_assistance': 'Subsidized premium (1.5-2% only)',
            'website': 'https://pmfby.gov.in',
            'icon': '🛡️'
        },
        {
            'name': 'Restructured Weather Based Crop Insurance Scheme (RWBCIS)',
            'name_hi': 'मौसम आधारित फसल बीमा योजना',
            'short_description': 'Weather-based insurance protecting against adverse weather conditions',
            'description': 'RWBCIS provides insurance based on weather parameters like rainfall, temperature, humidity, wind speed etc. Claims triggered automatically when weather deviates from normal.',
            'benefits': 'Protection against drought, excess rainfall, heat wave, frost, etc. Quick claim settlement based on weather data.',
            'eligibility': 'All farmers growing notified crops in notified areas',
            'application_process': 'Apply through banks or insurance company branches',
            'documents_required': 'Land Records, Bank Account Details',
            'category': 'insurance',
            'financial_assistance': 'Subsidized premium',
            'website': 'https://pmfby.gov.in',
            'icon': '🌦️'
        },
        
        # Credit & Loan Schemes
        {
            'name': 'Modified Interest Subvention Scheme (MISS) / Kisan Credit Card (KCC)',
            'name_hi': 'किसान क्रेडिट कार्ड योजना',
            'short_description': 'Concessional agricultural loans through Kisan Credit Card',
            'description': 'KCC scheme provides adequate and timely credit support to farmers under a single window. Farmers receive loans at subsidized interest rate of 7%. Prompt repayment reduces rate to 4%.',
            'benefits': 'Loans up to ₹3 lakh at 4% effective interest rate. Flexible withdrawal and repayment. Covers cultivation and other needs.',
            'eligibility': 'All farmers - individual/joint borrowers. Land-owning farmers, tenant farmers, sharecroppers.',
            'application_process': 'Apply at any bank branch with land records. Digital KCC also available.',
            'documents_required': 'Land Records, Identity Proof, Address Proof, Photograph',
            'category': 'credit_loan',
            'financial_assistance': 'Loans at 4% interest rate',
            'website': 'https://kcc.gov.in',
            'icon': '💳'
        },
        {
            'name': 'Agriculture Infrastructure Fund (AIF)',
            'name_hi': 'कृषि अवसंरचना कोष',
            'short_description': 'Financing for setting up post-harvest agricultural infrastructure',
            'description': 'AIF provides medium-long term debt financing for setting up community farming assets like warehousing, cold chains, processing units, etc.',
            'benefits': 'Loans up to ₹2 crore at 3% interest subvention. Moratorium up to 2 years. Credit guarantee coverage.',
            'eligibility': 'Farmers, FPOs, SHGs, cooperatives, agri-entrepreneurs, startups',
            'application_process': 'Apply through eligible lending institutions (banks, NBFCs)',
            'documents_required': 'Project Report, Identity Proof, Land Documents',
            'category': 'infrastructure',
            'financial_assistance': 'Loans with 3% interest subvention',
            'website': 'https://agriinfra.dac.gov.in',
            'icon': '🏗️'
        },
        
        # Infrastructure & Development
        {
            'name': 'Formation and Promotion of Farmer Producers Organizations (FPOs)',
            'name_hi': 'किसान उत्पादक संगठन योजना',
            'short_description': 'Promoting 10,000 new FPOs to enhance farmers\' collective bargaining power',
            'description': 'Scheme to establish 10,000 new FPOs across India to help farmers aggregate production, access better markets, and reduce input costs.',
            'benefits': 'Financial support up to ₹18 lakh per FPO. Equity grant up to ₹2,000 per farmer member. Credit guarantee facility.',
            'eligibility': 'Farmers interested in forming producer organization. Minimum 500 farmers per FPO.',
            'application_process': 'Apply through NABARD/SFAC/Small Farmers Agri-Business Consortium',
            'documents_required': 'Farmer Details, Area of Operation Plan',
            'category': 'marketing',
            'financial_assistance': '₹18 lakh financial support per FPO',
            'website': 'https://sfacindia.com',
            'icon': '👥'
        },
        {
            'name': 'Agriculture Infrastructure Fund (AIF)',
            'name_hi': 'कृषि अवसंरचना कोष',
            'short_description': 'Financing for setting up post-harvest agricultural infrastructure',
            'description': 'AIF provides medium-long term debt financing for setting up community farming assets like warehousing, cold chains, processing units, etc.',
            'benefits': 'Loans up to ₹2 crore at 3% interest subvention. Moratorium up to 2 years. Credit guarantee coverage.',
            'eligibility': 'Farmers, FPOs, SHGs, cooperatives, agri-entrepreneurs, startups',
            'application_process': 'Apply through eligible lending institutions (banks, NBFCs)',
            'documents_required': 'Project Report, Identity Proof, Land Documents',
            'category': 'infrastructure',
            'financial_assistance': 'Loans with 3% interest subvention',
            'website': 'https://agriinfra.dac.gov.in',
            'icon': '🏗️'
        },
        
        # Irrigation Schemes
        {
            'name': 'Per Drop More Crop (PDMC)',
            'name_hi': 'प्रति बूंद अधिक फसल',
            'short_description': 'Micro-irrigation scheme promoting drip and sprinkler irrigation',
            'description': 'PDMC promotes water use efficiency through micro-irrigation (drip and sprinkler systems). Part of Pradhan Mantri Krishi Sinchayee Yojana.',
            'benefits': 'Subsidy of 55% for small/marginal farmers, 45% for other farmers on micro-irrigation systems',
            'eligibility': 'All farmers with cultivable land and water source',
            'application_process': 'Apply through State Agriculture Department or PMKSY portal',
            'documents_required': 'Land Records, Water Source Details, Aadhaar Card',
            'category': 'irrigation',
            'financial_assistance': '45-55% subsidy on micro-irrigation systems',
            'website': 'https://pmksy.gov.in',
            'icon': '💧'
        },
        
        # Mechanization
        {
            'name': 'Sub-Mission on Agricultural Mechanization (SMAM)',
            'name_hi': 'कृषि यंत्रीकरण उप-मिशन',
            'short_description': 'Promoting farm mechanization through subsidies on agricultural equipment',
            'description': 'SMAM provides financial assistance for purchase of tractors, harvesters, seed drills, and other farm equipment. Promotes custom hiring centers.',
            'benefits': 'Up to 40-50% subsidy on farm equipment for individual farmers. Higher for SC/ST/women farmers.',
            'eligibility': 'All farmers, FPOs, Custom Hiring Centers, Cooperative Societies',
            'application_process': 'Apply through State Agriculture Department or District Agriculture Office',
            'documents_required': 'Land Records, Aadhaar Card, Bank Details',
            'category': 'mechanization',
            'financial_assistance': '40-50% subsidy on farm equipment',
            'website': 'https://agrimachinery.nic.in',
            'icon': '🚜'
        },
        
        # Organic Farming
        {
            'name': 'Paramparagat Krishi Vikas Yojana (PKVY)',
            'name_hi': 'परम्परागत कृषि विकास योजना',
            'short_description': 'Promoting organic farming and certification',
            'description': 'PKVY promotes cluster-based organic farming with end-to-end support from production to certification and marketing.',
            'benefits': '₹50,000 per hectare over 3 years. Support for organic inputs, certification, and marketing.',
            'eligibility': 'Farmers willing to adopt organic farming. Minimum 50 acres cluster.',
            'application_process': 'Apply through State Agriculture Department or NCOF',
            'documents_required': 'Land Records, Organic Farming Declaration',
            'category': 'organic_farming',
            'financial_assistance': '₹50,000 per hectare',
            'website': 'https://pkvy.gov.in',
            'icon': '🌱'
        },
        {
            'name': 'National Mission on Natural Farming (NMNF)',
            'name_hi': 'राष्ट्रीय प्राकृतिक खेती मिशन',
            'short_description': 'Promoting chemical-free natural farming practices',
            'description': 'NMNF promotes natural farming techniques without synthetic chemicals. Focus on indigenous cows, multi-cropping, and soil health.',
            'benefits': 'Financial support for input procurement, training, demonstration plots, and certification.',
            'eligibility': 'Farmers adopting natural farming practices',
            'application_process': 'Apply through State Agriculture Department',
            'documents_required': 'Land Records, Natural Farming Declaration',
            'category': 'organic_farming',
            'financial_assistance': 'Support for inputs and training',
            'website': 'https://nmnf.dac.gov.in',
            'icon': '🌿'
        },
        
        # Soil Health
        {
            'name': 'Soil Health & Fertility (SH&F)',
            'name_hi': 'मृदा स्वास्थ्य एवं उर्वरकता',
            'short_description': 'Soil Health Card scheme for soil testing and nutrient management',
            'description': 'Scheme provides Soil Health Cards to farmers every 2 years with nutrient status and fertilizer recommendations.',
            'benefits': 'Free soil testing, customized fertilizer recommendations, training on soil health management.',
            'eligibility': 'All farmers',
            'application_process': 'Contact local Agriculture Department or Krishi Vigyan Kendra for soil sample collection',
            'documents_required': 'Land details',
            'category': 'seed_planting',
            'financial_assistance': 'Free soil testing',
            'website': 'https://soilhealth.dac.gov.in',
            'icon': '🧪'
        },
        
        # Digital Agriculture
        {
            'name': 'Digital Agriculture Mission',
            'name_hi': 'डिजिटल कृषि मिशन',
            'short_description': 'Creating digital infrastructure for agriculture sector',
            'description': 'Digital Agriculture Mission creates Farmer IDs (Kisan Pehchaan Patra) linked to land records, crop details, and schemes availed.',
            'benefits': 'Digital identity for farmers. Easy access to schemes. Unified portal for all agriculture services.',
            'eligibility': 'All farmers',
            'application_process': 'Register online at Digital Agriculture Mission portal or through CSC',
            'documents_required': 'Aadhaar Card, Land Records',
            'category': 'digital_agri',
            'financial_assistance': 'N/A',
            'website': 'https://agristack.gov.in',
            'icon': '📱'
        },
        
        # Horticulture
        {
            'name': 'Mission for Integrated Development of Horticulture (MIDH)',
            'name_hi': 'बागवानी एकीकृत विकास मिशन',
            'short_description': 'Support for horticulture crops - fruits, vegetables, flowers, spices',
            'description': 'MIDH provides financial assistance for area expansion, production of planting material, creation of post-harvest infrastructure, and marketing of horticulture produce.',
            'benefits': 'Subsidy up to 50-85% on various horticulture interventions depending on crop and farmer category.',
            'eligibility': 'All farmers, FPOs, cooperatives, nurseries',
            'application_process': 'Apply through State Horticulture Mission office',
            'documents_required': 'Land Records, Proposed Activity Details',
            'category': 'horticulture',
            'financial_assistance': '50-85% subsidy',
            'website': 'https://midh.gov.in',
            'icon': '🍎'
        },
        
        # Marketing Schemes
        {
            'name': 'Pradhan Mantri Annadata Aay Sanrakshan Abhiyan (PM-AASHA)',
            'name_hi': 'प्रधानमंत्री अन्नदाता आय संरक्षण अभियान',
            'short_description': 'Ensuring remunerative prices for farmers through MSP operations',
            'description': 'PM-AASHA ensures farmers get Minimum Support Price (MSP) for their produce through Price Support Scheme, Price Deficiency Payment Scheme, and Private Procurement Stockist Scheme.',
            'benefits': 'MSP assurance for notified crops. Direct payment of price deficiency to farmers.',
            'eligibility': 'All farmers growing notified crops',
            'application_process': 'Register with state procurement agencies',
            'documents_required': 'Land Records, Aadhaar Card, Bank Details',
            'category': 'marketing',
            'financial_assistance': 'MSP guarantee',
            'website': 'https://pm-aasha.dac.gov.in',
            'icon': '📈'
        },
        {
            'name': 'Integrated Scheme for Agriculture Marketing (ISAM)',
            'name_hi': 'एकीकृत कृषि विपणन योजना',
            'short_description': 'Strengthening agricultural marketing infrastructure',
            'description': 'ISAM supports development of agricultural marketing infrastructure including e-NAM (National Agriculture Market), warehouses, grading units, and rural haats.',
            'benefits': 'Financial assistance for market infrastructure. Access to pan-India trading through e-NAM.',
            'eligibility': 'Farmers, traders, market committees, FPOs',
            'application_process': 'Apply through State Marketing Board or e-NAM portal',
            'documents_required': 'Entity registration details',
            'category': 'marketing',
            'financial_assistance': 'Subsidy on marketing infrastructure',
            'website': 'https://enam.gov.in',
            'icon': '🏪'
        },
        
        # New initiatives (2025-26)
        {
            'name': 'Namo Drone Didi',
            'name_hi': 'नमो ड्रोन दीदी',
            'short_description': 'Providing drones to women Self Help Groups for agricultural spraying',
            'description': 'Namo Drone Didi provides drones to 15,000 women SHGs across India for agricultural spraying of fertilizers and pesticides.',
            'benefits': 'Drone training and equipment to women SHGs. Financial support for procurement.',
            'eligibility': 'Women Self Help Groups registered under DAY-NRLM',
            'application_process': 'Apply through State Rural Livelihoods Mission',
            'documents_required': 'SHG Registration Documents',
            'category': 'mechanization',
            'financial_assistance': 'Up to 80% subsidy on drone procurement',
            'website': 'https://nrlm.gov.in',
            'icon': '🚁'
        },
        {
            'name': 'Mission for Aatmanirbharta in Pulses',
            'name_hi': 'दलहन में आत्मनिर्भरता मिशन',
            'short_description': 'Achieving self-sufficiency in Tur, Urad, and Masoor pulses production',
            'description': 'Mission to enhance pulses production with focus on Tur, Urad, Masoor. ₹11,440 crore outlay over 6 years (2025-26 to 2030-31).',
            'benefits': 'Climate-resilient seeds, area expansion, processing units, procurement support at MSP.',
            'eligibility': 'Farmers growing pulses (Tur, Urad, Masoor) in identified districts',
            'application_process': 'Contact State Agriculture Department',
            'documents_required': 'Land Records',
            'category': 'seed_planting',
            'financial_assistance': 'Free seed kits, post-harvest support',
            'website': 'https://agricoop.nic.in',
            'icon': '🫘'
        },
        
        # Additional Important Schemes
        {
            'name': 'National Mission on Edible Oils (NMEO) - Oil Palm',
            'name_hi': 'राष्ट्रीय खाद्य तेल मिशन - ताड़ तेल',
            'short_description': 'Promoting oil palm cultivation to reduce edible oil imports',
            'description': 'NMEO-Oil Palm aims to increase area under oil palm cultivation to 10 lakh hectares with financial support for planting material, irrigation, and processing units.',
            'benefits': 'Subsidy up to ₹37,000 per hectare. Price assurance for Fresh Fruit Bunches.',
            'eligibility': 'Farmers in oil palm-growing states',
            'application_process': 'Apply through State Horticulture Mission',
            'documents_required': 'Land Records',
            'category': 'horticulture',
            'financial_assistance': '₹37,000 per hectare subsidy',
            'website': 'https://nmeo.dac.gov.in',
            'icon': '🌴'
        },
        {
            'name': 'National Mission on Edible Oils (NMEO) - Oilseeds',
            'name_hi': 'राष्ट्रीय खाद्य तेल मिशन - तिलहन',
            'short_description': 'Promoting oilseeds production for self-reliance in edible oils',
            'description': 'NMEO-Oilseeds focuses on increasing production of traditional oilseeds like groundnut, soybean, mustard, sunflower, sesamum, and safflower.',
            'benefits': 'SEPs (Seed hubs, Extension, Price support), cluster demonstration, post-harvest support.',
            'eligibility': 'Farmers growing oilseeds in identified districts',
            'application_process': 'Contact State Agriculture Department',
            'documents_required': 'Land Records',
            'category': 'seed_planting',
            'financial_assistance': 'SEP support',
            'website': 'https://nmeo.dac.gov.in',
            'icon': '🌻'
        },
        {
            'name': 'National Bamboo Mission',
            'name_hi': 'राष्ट्रीय बांस मिशन',
            'short_description': 'Promoting bamboo cultivation and processing',
            'description': 'National Bamboo Mission aims to increase area under bamboo, improve quality of planting material, and establish processing units.',
            'benefits': 'Subsidy up to 60% on bamboo plantation. Support for nurseries, processing units, and market linkages.',
            'eligibility': 'Farmers, FPOs, cooperatives in bamboo-growing states',
            'application_process': 'Apply through State Bamboo Mission office',
            'documents_required': 'Land Records',
            'category': 'horticulture',
            'financial_assistance': 'Up to 60% subsidy',
            'website': 'https://nbm.nic.in',
            'icon': '🎋'
        },
        {
            'name': 'Crop Diversification Programme (CDP)',
            'name_hi': 'फसल विविधीकरण कार्यक्रम',
            'short_description': 'Encouraging shift from water-intensive paddy to less water-intensive crops',
            'description': 'CDP promotes diversification from paddy to alternative crops like pulses, oilseeds, and coarse grains in the green revolution states.',
            'benefits': 'Financial assistance for crop diversification, direct benefit transfer to farmers.',
            'eligibility': 'Farmers in identified districts',
            'application_process': 'Contact State Agriculture Department',
            'documents_required': 'Land Records',
            'category': 'seed_planting',
            'financial_assistance': 'Crop-specific support',
            'website': 'https://agricoop.nic.in',
            'icon': '🔄'
        },
        {
            'name': 'National Bee Keeping and Honey Mission (NBHM)',
            'name_hi': 'राष्ट्रीय मधुमक्खी पालन और शहद मिशन',
            'short_description': 'Promoting beekeeping for honey production and pollination services',
            'description': 'NBHM aims to increase honey production, support beekeepers, and promote scientific beekeeping practices.',
            'benefits': 'Subsidy on bee boxes and equipment. Training and certification support.',
            'eligibility': 'Farmers, SHGs, cooperatives, agri-entrepreneurs',
            'application_process': 'Apply through State Horticulture Mission or Khadi Village Industries Commission',
            'documents_required': 'Identity Proof, Training Certificate (if any)',
            'category': 'horticulture',
            'financial_assistance': 'Subsidy up to 40-50% on bee equipment',
            'website': 'https://kviconline.gov.in',
            'icon': '🐝'
        },
        {
            'name': 'Agri Fund for Start-Ups & Rural Enterprises (AgriSURE)',
            'name_hi': 'कृषि स्टार्टअप एवं ग्रामीण उद्यम कोष',
            'short_description': 'Venture capital fund for agri-startups and rural enterprises',
            'description': 'AgriSURE is a venture capital fund supporting innovative startups in agriculture and allied sectors.',
            'benefits': 'Equity funding for agri-startups. Mentorship and market access support.',
            'eligibility': 'Agri-startups, rural enterprises, agri-tech companies',
            'application_process': 'Apply online through AgriSURE website',
            'documents_required': 'Business Plan, Registration Certificate',
            'category': 'infrastructure',
            'financial_assistance': 'Venture capital funding',
            'website': 'https://agrisure.in',
            'icon': '💼'
        }
    ]
    
    # Remove duplicates by using a set of names
    unique_schemes = {}
    for scheme in schemes_data:
        if scheme['name'] not in unique_schemes:
            unique_schemes[scheme['name']] = scheme
    
    # Create/update schemes
    created_count = 0
    updated_count = 0
    
    for scheme_data in unique_schemes.values():
        scheme, created = GovernmentScheme.objects.update_or_create(
            name=scheme_data['name'],
            defaults=scheme_data
        )
        if created:
            created_count += 1
            print(f"✓ Created: {scheme.name}")
        else:
            updated_count += 1
            print(f"● Updated: {scheme.name}")
    
    print("\n" + "="*50)
    print("✅ SCHEMES POPULATED SUCCESSFULLY!")
    print(f"📊 Total Schemes: {GovernmentScheme.objects.count()}")
    print(f"🆕 Created: {created_count}")
    print(f"🔄 Updated: {updated_count}")
    print("="*50)
    
    # Print category-wise count
    print("\n📂 Category-wise breakdown:")
    from collections import Counter
    categories = Counter(GovernmentScheme.objects.values_list('category', flat=True))
    for category, count in categories.items():
        print(f"  - {category}: {count} schemes")

if __name__ == '__main__':
    populate_schemes()
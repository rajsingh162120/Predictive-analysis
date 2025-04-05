
import React, { useState } from 'react';

const LegalCasePredictor = () => {
  // State management
  const [caseDetails, setCaseDetails] = useState({
    title: "Property Tax Exemption Dispute - Charitable Trust",
    type: "Tax",
    description: "Challenging tax authority's denial of property tax exemption for a charitable educational institution. The trust has operated for 15 years providing subsidized education to economically disadvantaged students."
  });
  
  const [evidenceItems, setEvidenceItems] = useState([
    {
      description: "Trust registration documents showing charitable purpose",
      type: "document",
      reliability: 5,
      relevance: 5,
      strength_score: 92.5,
      category: "Very Strong"
    },
    {
      description: "15 years of annual financial statements with proper audits",
      type: "financial",
      reliability: 5,
      relevance: 5,
      strength_score: 90.0,
      category: "Very Strong"
    },
    {
      description: "Tax exemption certificates from previous years",
      type: "document",
      reliability: 5,
      relevance: 5,
      strength_score: 85.0,
      category: "Very Strong"
    },
    {
      description: "Testimonials from beneficiary students and families",
      type: "witness",
      reliability: 4,
      relevance: 4,
      strength_score: 70.0,
      category: "Strong"
    },
    {
      description: "Expert testimony from tax law professor",
      type: "expert",
      reliability: 5,
      relevance: 5,
      strength_score: 87.5,
      category: "Very Strong"
    },
    {
      description: "Operational records showing educational activities",
      type: "document",
      reliability: 4,
      relevance: 5,
      strength_score: 82.5,
      category: "Very Strong"
    }
  ]);
  
  const [strategy, setStrategy] = useState(
    "Our strategy focuses on establishing the clear charitable nature of the institution through documentary evidence and expert testimony. We will emphasize consistent compliance with all statutory requirements for tax exemption over 15 years. We'll cite relevant precedents from the Supreme Court affirming exemptions for similar educational trusts. We'll challenge the tax authority's new interpretation of the exemption criteria as being inconsistent with legislative intent and prior administrative practice."
  );
  
  const [pdfText, setPdfText] = useState('');
  const [extractedData, setExtractedData] = useState(null);
  const [fileUploaded, setFileUploaded] = useState(false);
  
  // Mock PDF extraction function
  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      // In a real app, this would use PDF.js or a similar library
      // For this demo, we'll simulate PDF content
      const reader = new FileReader();
      reader.onload = () => {
        setFileUploaded(true);
        setTimeout(() => {
          setPdfText("CHARITABLE EDUCATIONAL TRUST\nTAX EXEMPTION APPLICATION\n\nTrust Registration: #TR-12345-2008\nDate of Establishment: March 15, 2008\n\nTrust Activities:\n- Providing subsidized education to economically disadvantaged students\n- Scholarship programs for 120+ students annually\n- Vocational training programs\n\nFinancial Statement Summary:\nAnnual Income: Rs. 45,28,000\nExpenditure on Charitable Activities: Rs. 42,15,000 (93%)\nAdministrative Expenses: Rs. 3,13,000 (7%)\n\nCompliance History:\n- Filed returns consistently for 15 years\n- Previous exemptions granted under Section 12A\n- Audit reports show no fund diversions\n\nGrounds for Current Dispute:\nTax authority claims change in activity proportion, despite consistent operations.");
          extractData();
        }, 1000);
      };
      reader.readAsText(file);
    }
  };
  
  // Extract relevant data from PDF text based on parameters
  const extractData = () => {
    // In a real implementation, this would use NLP or regex patterns
    // For demo purposes, we'll simulate extraction
    setExtractedData({
      entity_name: "Charitable Educational Trust",
      registration_details: {
        number: "TR-12345-2008",
        date: "March 15, 2008"
      },
      charitable_activities: [
        "Providing subsidized education to economically disadvantaged students",
        "Scholarship programs for 120+ students annually",
        "Vocational training programs"
      ],
      financial_summary: {
        annual_income: "Rs. 45,28,000",
        charitable_expenditure: "Rs. 42,15,000 (93%)",
        administrative_expenses: "Rs. 3,13,000 (7%)"
      },
      compliance_history: {
        consistent_filings: true,
        exemption_section: "12A",
        audit_findings: "No fund diversions"
      },
      dispute_grounds: "Tax authority claims change in activity proportion, despite consistent operations"
    });
  };
  
  // Add extracted elements to evidence portfolio
  const addExtractedEvidence = () => {
    if (!extractedData) return;
    
    const newEvidence = [
      {
        description: `Registration certificate #${extractedData.registration_details.number}`,
        type: "document",
        reliability: 5,
        relevance: 5,
        strength_score: 95.0,
        category: "Very Strong"
      },
      {
        description: `Financial records showing ${extractedData.financial_summary.charitable_expenditure} spent on charitable activities`,
        type: "financial",
        reliability: 5,
        relevance: 5,
        strength_score: 97.5,
        category: "Very Strong"
      }
    ];
    
    setEvidenceItems([...evidenceItems, ...newEvidence]);
  };
  
  // Analysis results
  const predictionResults = {
    win_probability: {
      win_probability: 85.0,
      base_case_probability: 82.5,
      evidence_contribution: 28.5,
      strategy_contribution: 16.0
    },
    outcome_analysis: {
      outcome_category: "Highly Favorable",
      outcome_description: "Strong likelihood of success based on compelling evidence, effective strategy, and favorable precedents.",
      key_positive_factors: [
        "Exceptional documentary evidence showing consistent charitable operations",
        "Strong precedents with 90%+ similarity having favorable outcomes",
        "Expert testimony strengthening legal interpretation arguments",
        "15-year history of tax compliance and previous exemption approvals"
      ],
      key_negative_factors: [
        "Recent administrative policy change creating some uncertainty",
        "Limited evidence addressing specific grounds for current denial"
      ],
      judicial_considerations: [
        "Likely to give substantial weight to consistent prior tax treatment",
        "Likely to scrutinize tax authority's justification for policy change",
        "Likely to consider precedent cases from Supreme Court on similar educational trusts"
      ]
    },
    evidence_analysis: {
      evidence_items: evidenceItems,
      overall_score: 86.3,
      overall_category: "Very Strong",
      portfolio_gaps: [
        "Limited evidence addressing specific grounds cited in current exemption denial",
        "No comparative evidence from similar charitable trusts facing same issue"
      ],
      portfolio_strengths: [
        "Multiple strong documentary evidence items (5)",
        "Strong expert testimony with direct tax law relevance",
        "Comprehensive financial documentation spanning full operational period"
      ]
    },
    strategy_analysis: {
      primary_strategy: "substantive",
      secondary_strategy: "legal_interpretation",
      strategy_scores: {
        procedural: 0.15,
        substantive: 0.35,
        aggressive: 0.10,
        defensive: 0.15,
        settlement_oriented: 0.05,
        fact_based: 0.30,
        legal_interpretation: 0.25
      },
      strategy_balance: "Well-balanced strategy covering multiple approaches",
      strategy_gaps: [
        "Limited procedural challenge to tax authority's review process",
        "Minimal settlement-oriented approach as fallback position"
      ],
      strategy_effectiveness: "High - Facts supported by legal precedent is compelling"
    },
    similar_cases: [
      {
        title: "Adarsh Educational Society v. Commissioner of Income Tax",
        similarity: 0.92,
        outcome: "Favorable",
        key_factors: [
          "Long-standing history of charitable operations",
          "Consistent tax compliance",
          "Strong documentary evidence",
          "Demonstration that 85%+ of funds used for charitable purpose"
        ],
        evidence_strength: "Very Strong",
        strategy_used: "Fact-based with legal interpretation focus"
      },
      {
        title: "Saraswati Educational Trust v. Tax Authority",
        similarity: 0.88,
        outcome: "Favorable",
        key_factors: [
          "Educational institution with similar beneficiary profile",
          "Challenged policy interpretation successfully",
          "Provided comparative analysis with other exempted institutions"
        ],
        evidence_strength: "Strong",
        strategy_used: "Legal interpretation with procedural challenges"
      },
      {
        title: "Modern Education Society v. State Tax Board",
        similarity: 0.85,
        outcome: "Favorable",
        key_factors: [
          "Supreme Court precedent citations",
          "Expert testimony on tax law",
          "Constitutional arguments on charitable purpose"
        ],
        evidence_strength: "Strong",
        strategy_used: "Legal interpretation with constitutional arguments"
      },
      {
        title: "National Education Foundation v. Revenue Department",
        similarity: 0.79,
        outcome: "Partially Favorable",
        key_factors: [
          "Similar charitable purpose but inconsistent documentation",
          "Weaker financial segregation of activities",
          "Partial exemption granted"
        ],
        evidence_strength: "Moderate",
        strategy_used: "Primarily substantive without strong procedural elements"
      },
      {
        title: "Progressive Learning Trust v. Tax Authority",
        similarity: 0.72,
        outcome: "Favorable",
        key_factors: [
          "Established charitable intent",
          "Strong witness testimony from beneficiaries",
          "Previous tax exemption history"
        ],
        evidence_strength: "Strong",
        strategy_used: "Fact-based with witness testimony focus"
      }
    ],
    recommendations: [
      {
        category: "Evidence",
        priority: "High",
        recommendation: "Obtain comparative evidence from similar charitable trusts that maintained exemption",
        rationale: "Demonstrates inconsistent application of policy by tax authority"
      },
      {
        category: "Evidence",
        priority: "High",
        recommendation: "Secure affidavit from tax authority officials who previously approved exemptions",
        rationale: "Establishes administrative precedent and consistency in operations"
      },
      {
        category: "Strategy",
        priority: "Moderate",
        recommendation: "Add procedural challenge to the tax authority's review methodology",
        rationale: "Creates additional grounds for favorable ruling"
      },
      {
        category: "Case Strategy",
        priority: "Moderate",
        recommendation: "Incorporate constitutional arguments about equal protection as used in Adarsh Educational Society case",
        rationale: "This approach was successful in a case with 92% similarity"
      },
      {
        category: "Evidence Improvement",
        priority: "Moderate",
        recommendation: "Strengthen student testimonials by focusing on specific educational outcomes",
        rationale: "Creates stronger connection between charitable purpose and activities"
      }
    ]
  };

  // Generate PDF report of analysis
  const generateReport = () => {
    alert("Report generation initiated - in a full implementation, this would download a PDF report with all analysis details");
  };

  return (
    <div className="p-6 max-w-6xl mx-auto bg-white rounded-xl shadow-md">
      <h1 className="text-2xl font-bold mb-6 text-center">⚖️ Legal Case Outcome Predictor</h1>
      
      {/* Case Details */}
      <div className="mb-8 bg-gray-50 p-4 rounded-lg">
        <h2 className="text-xl font-semibold mb-3">📝 Case Details</h2>
        <p><strong>Title:</strong> {caseDetails.title}</p>
        <p><strong>Type:</strong> {caseDetails.type}</p>
        <p><strong>Description:</strong> {caseDetails.description}</p>
      </div>
      
      {/* PDF Extraction */}
      <div className="mb-8 bg-blue-50 p-4 rounded-lg">
        <h2 className="text-xl font-semibold mb-3">📄 Document Analysis</h2>
        <p className="mb-3">Upload case documents to automatically extract key information:</p>
        
        <input
          type="file"
          accept=".pdf"
          onChange={handleFileUpload}
          className="mb-4 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
        />
        
        {fileUploaded && !extractedData && (
          <div className="flex items-center justify-center py-4">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-700"></div>
            <span className="ml-3">Analyzing document...</span>
          </div>
        )}
        
        {extractedData && (
          <div className="mt-4">
            <h3 className="font-semibold text-lg mb-2">Extracted Data:</h3>
            <div className="bg-white p-3 rounded-md border border-gray-200">
              <p><strong>Entity:</strong> {extractedData.entity_name}</p>
              <p><strong>Registration:</strong> {extractedData.registration_details.number} ({extractedData.registration_details.date})</p>
              
              <div className="mt-2">
                <strong>Charitable Activities:</strong>
                <ul className="list-disc ml-5">
                  {extractedData.charitable_activities.map((activity, idx) => (
                    <li key={idx}>{activity}</li>
                  ))}
                </ul>
              </div>
              
              <div className="mt-2">
                <strong>Financial Summary:</strong>
                <ul className="list-disc ml-5">
                  <li>Income: {extractedData.financial_summary.annual_income}</li>
                  <li>Charitable Expenditure: {extractedData.financial_summary.charitable_expenditure}</li>
                  <li>Administrative: {extractedData.financial_summary.administrative_expenses}</li>
                </ul>
              </div>
              
              <p className="mt-2"><strong>Dispute Grounds:</strong> {extractedData.dispute_grounds}</p>
              
              <button 
                onClick={addExtractedEvidence}
                className="mt-3 bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700">
                Add Extracted Evidence to Portfolio
              </button>
            </div>
          </div>
        )}
      </div>
      
      {/* Evidence Portfolio */}
      <div className="mb-8 bg-gray-50 p-4 rounded-lg">
        <h2 className="text-xl font-semibold mb-3">🧾 Evidence Portfolio</h2>
        
        <div className="overflow-auto">
          <table className="min-w-full bg-white">
            <thead className="bg-gray-100">
              <tr>
                <th className="py-2 px-4 border-b text-left">Description</th>
                <th className="py-2 px-4 border-b text-left">Type</th>
                <th className="py-2 px-4 border-b text-center">Strength</th>
                <th className="py-2 px-4 border-b text-center">Category</th>
              </tr>
            </thead>
            <tbody>
              {evidenceItems.map((item, index) => (
                <tr key={index} className={index % 2 === 0 ? 'bg-gray-50' : 'bg-white'}>
                  <td className="py-2 px-4 border-b">{item.description}</td>
                  <td className="py-2 px-4 border-b">{item.type}</td>
                  <td className="py-2 px-4 border-b text-center">{item.strength_score}%</td>
                  <td className="py-2 px-4 border-b text-center">
                    <span className={`inline-block px-2 py-1 rounded-full text-xs 
                      ${item.category === 'Very Strong' && 'bg-green-100 text-green-800'}
                      ${item.category === 'Strong' && 'bg-blue-100 text-blue-800'}
                      ${item.category === 'Moderate' && 'bg-yellow-100 text-yellow-800'}
                      ${item.category === 'Weak' && 'bg-orange-100 text-orange-800'}
                      ${item.category === 'Very Weak' && 'bg-red-100 text-red-800'}
                    `}>
                      {item.category}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        
        <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-white p-3 rounded-md border border-gray-200">
            <h3 className="font-semibold">Portfolio Gaps</h3>
            <ul className="list-disc ml-5 mt-2">
              {predictionResults.evidence_analysis.portfolio_gaps.map((gap, idx) => (
                <li key={idx}>{gap}</li>
              ))}
            </ul>
          </div>
          <div className="bg-white p-3 rounded-md border border-gray-200">
            <h3 className="font-semibold">Portfolio Strengths</h3>
            <ul className="list-disc ml-5 mt-2">
              {predictionResults.evidence_analysis.portfolio_strengths.map((strength, idx) => (
                <li key={idx}>{strength}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>
      
      {/* Legal Strategy */}
      <div className="mb-8 bg-gray-50 p-4 rounded-lg">
        <h2 className="text-xl font-semibold mb-3">⚔️ Legal Strategy</h2>
        <p className="mb-4">{strategy}</p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-white p-3 rounded-md border border-gray-200">
            <h3 className="font-semibold">Strategy Analysis</h3>
            <p className="mt-2"><strong>Primary Approach:</strong> {predictionResults.strategy_analysis.primary_strategy}</p>
            <p><strong>Secondary Approach:</strong> {predictionResults.strategy_analysis.secondary_strategy}</p>
            <p><strong>Balance:</strong> {predictionResults.strategy_analysis.strategy_balance}</p>
            <p><strong>Effectiveness:</strong> {predictionResults.strategy_analysis.strategy_effectiveness}</p>
          </div>
          <div className="bg-white p-3 rounded-md border border-gray-200">
            <h3 className="font-semibold">Strategy Gaps</h3>
            <ul className="list-disc ml-5 mt-2">
              {predictionResults.strategy_analysis.strategy_gaps.map((gap, idx) => (
                <li key={idx}>{gap}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>
      
      {/* Outcome Prediction */}
      <div className="mb-8 bg-blue-50 p-4 rounded-lg">
        <h2 className="text-xl font-semibold mb-3">📊 Outcome Prediction</h2>
        
        <div className="flex flex-col md:flex-row">
          <div className="w-full md:w-1/3 text-center">
            <div className="bg-white rounded-lg p-4 shadow-sm mb-4">
              <h3 className="text-2xl font-bold text-blue-800">{predictionResults.win_probability.win_probability}%</h3>
              <div className="w-full bg-gray-200 rounded-full h-4 mt-2">
                <div 
                  className="bg-blue-600 h-4 rounded-full" 
                  style={{width: `${predictionResults.win_probability.win_probability}%`}}
                ></div>
              </div>
              <p className="mt-2 text-gray-700">Favorable Outcome Probability</p>
              <p className="mt-1 text-sm font-semibold">{predictionResults.outcome_analysis.outcome_category}</p>
            </div>
          </div>
          
          <div className="w-full md:w-2/3 md:pl-6">
            <p className="mb-3">{predictionResults.outcome_analysis.outcome_description}</p>
            
            <div className="mb-4">
              <h3 className="font-semibold">Key Positive Factors:</h3>
              <ul className="list-disc ml-5">
                {predictionResults.outcome_analysis.key_positive_factors.map((factor, idx) => (
                  <li key={idx} className="text-green-700">{factor}</li>
                ))}
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold">Key Negative Factors:</h3>
              <ul className="list-disc ml-5">
                {predictionResults.outcome_analysis.key_negative_factors.map((factor, idx) => (
                  <li key={idx} className="text-red-700">{factor}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
      
      {/* Similar Cases */}
      <div className="mb-8 bg-gray-50 p-4 rounded-lg">
        <h2 className="text-xl font-semibold mb-3">📚 Similar Cases</h2>
        
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white">
            <thead className="bg-gray-100">
              <tr>
                <th className="py-2 px-4 border-b text-left">Case</th>
                <th className="py-2 px-4 border-b text-center">Similarity</th>
                <th className="py-2 px-4 border-b text-center">Outcome</th>
                <th className="py-2 px-4 border-b text-left">Key Factors</th>
              </tr>
            </thead>
            <tbody>
              {predictionResults.similar_cases.map((case_item, index) => (
                <tr key={index} className={index % 2 === 0 ? 'bg-gray-50' : 'bg-white'}>
                  <td className="py-2 px-4 border-b font-medium">{case_item.title}</td>
                  <td className="py-2 px-4 border-b text-center">{(case_item.similarity * 100).toFixed(0)}%</td>
                  <td className="py-2 px-4 border-b text-center">
                    <span className={`inline-block px-2 py-1 rounded-full text-xs
                      ${case_item.outcome === 'Favorable' && 'bg-green-100 text-green-800'}
                      ${case_item.outcome === 'Partially Favorable' && 'bg-yellow-100 text-yellow-800'}
                      ${case_item.outcome === 'Unfavorable' && 'bg-red-100 text-red-800'}
                    `}>
                      {case_item.outcome}
                    </span>
                  </td>
                  <td className="py-2 px-4 border-b">
                    <ul className="list-disc ml-4 text-sm">
                      {case_item.key_factors.map((factor, idx) => (
                        <li key={idx}>{factor}</li>
                      ))}
                    </ul>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      
      {/* Strategic Recommendations */}
      <div className="mb-8 bg-green-50 p-4 rounded-lg">
        <h2 className="text-xl font-semibold mb-3">🎯 Strategic Recommendations</h2>
        
        <div className="space-y-4">
          {["High", "Moderate"].map(priority => {
            const priorityRecs = predictionResults.recommendations.filter(r => r.priority === priority);
            if (priorityRecs.length === 0) return null;
            
            return (
              <div key={priority} className="bg-white p-3 rounded-md border border-gray-200">
                <h3 className="font-semibold text-lg mb-2">{priority} Priority</h3>
                {priorityRecs.map((rec, idx) => (
                  <div key={idx} className="mb-3 pl-3 border-l-4 border-green-500">
                    <p className="font-medium">{rec.recommendation}</p>
                    <p className="text-sm text-gray-600 mt-1">{rec.rationale}</p>
                  </div>
                ))}
              </div>
            );
          })}
        </div>
      </div>
      
      {/* Action Buttons */}
      <div className="flex justify-center mt-6">
        <button
          onClick={generateReport}
          className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 shadow-md">
          Generate Detailed Case Report
        </button>
      </div>
    </div>
  );
};

export default LegalCasePredictor;
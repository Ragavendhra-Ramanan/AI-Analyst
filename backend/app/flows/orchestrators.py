"""Flow orchestrators for PDF processing and benchmarking."""

import os
from datetime import datetime
from ..config.settings import BUCKET_NAME
from ..services.benchmark_creation.gcp_service import gcp_service
from ..services.benchmark_creation.vision_service import vision_service
from ..services.benchmark_creation.gemini_service import gemini_service
from ..services.benchmark_creation.firestore_service import firestore_service
from ..data.processors import metrics_processor
from ..data.analyzers import competitive_analyzer
from ..visualizations.charts import chart_generator
from ..visualizations.comparisons import comparison_visualizer
from ..visualizations.reports import pdf_report_generator


class PDFProcessingFlow:
    """Orchestrator for PDF processing and storage flow."""

    def __init__(self):
        pass

    def process_pdfs_from_folder(self, folder_path):
        """Process all PDFs in a folder and store in vector store."""
        try:
            print(f"Processing PDFs from folder: {folder_path}")

            if not os.path.exists(folder_path):
                print(f"Error: Folder {folder_path} does not exist")
                return False

            # Check service availability
            if not gcp_service.is_available():
                print("Google Cloud Storage service not available")
                return False

            if not vision_service.is_available():
                print("Google Vision API service not available")
                return False

            if not gemini_service.is_available():
                print("Gemini AI service not available")
                return False

            if not firestore_service.is_available():
                print("Firestore service not available")
                return False

            # Get all PDF files
            pdf_files = [
                f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")
            ]

            if not pdf_files:
                print("No PDF files found in the folder")
                return False

            print(f"Found {len(pdf_files)} PDF files to process")

            successful_count = 0

            for pdf_file in pdf_files:
                try:
                    pdf_path = os.path.join(folder_path, pdf_file)
                    print(f"\nProcessing: {pdf_file}")

                    # Upload to GCS
                    blob_name = f"pdfs/{pdf_file}"
                    if not gcp_service.upload_file(pdf_path, blob_name):
                        print(f"Failed to upload {pdf_file} to GCS")
                        continue

                    # Extract text using Vision API
                    gcs_uri = f"gs://{BUCKET_NAME}/{blob_name}"
                    extracted_text = vision_service.extract_text_from_pdf(gcs_uri)

                    if not extracted_text:
                        print(f"Failed to extract text from {pdf_file}")
                        continue

                    # Extract structured data using Gemini
                    structured_data = gemini_service.extract_structured_data(
                        extracted_text, pdf_file
                    )

                    if not structured_data:
                        print(f"Failed to extract structured data from {pdf_file}")
                        continue

                    # Store in Firestore
                    stored_doc_id = firestore_service.store_memo(
                        structured_data, pdf_file
                    )

                    if stored_doc_id:
                        print(f"Successfully processed and stored: {pdf_file}")
                        successful_count += 1
                    else:
                        print(f"Failed to store {pdf_file} in Firestore")

                except Exception as e:
                    print(f"Error processing {pdf_file}: {e}")
                    continue

            print(
                f"\nProcessing complete. Successfully processed {successful_count} out of {len(pdf_files)} PDFs"
            )
            return successful_count > 0

        except Exception as e:
            print(f"Error in PDF processing flow: {e}")
            return False


class BenchmarkingFlow:
    """Orchestrator for benchmarking analysis flow."""

    def __init__(self):
        pass

    def create_benchmark_analysis(self, memo_text, output_dir="benchmark_output"):
        """Create benchmark analysis from memo text."""
        try:
            print("Starting benchmark analysis...")

            # Check service availability
            if not gemini_service.is_available():
                print("Gemini AI service not available")
                return None

            if not firestore_service.is_available():
                print("Firestore service not available")
                return None

            # Create output directory
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Extract structured data from memo
            print("Extracting structured data from memo...")
            target_company_data = gemini_service.extract_structured_data(
                memo_text, "memo_input"
            )

            if not target_company_data:
                print("Failed to extract structured data from memo")
                return None

            # Extract sector information
            sector_hierarchy = target_company_data.get("company_overview", {}).get(
                "sector_hierarchy", []
            )
            if not sector_hierarchy:
                print("No sector information found in memo")
                return None

            sector = sector_hierarchy[-1] if sector_hierarchy else ""
            print(f"Target sector: {sector}")

            # Get competitor companies from Firestore
            print("Retrieving competitor companies from database...")
            competitor_companies = firestore_service.get_sector_competitors(
                target_company_data
            )

            if not competitor_companies:
                print(f"No competitor companies found for sector: {sector}")
                return None

            print(f"Found {len(competitor_companies)} competitor companies")

            # Prepare comparison data
            print("Preparing comparison data...")
            comparison_df = metrics_processor.prepare_comparison_data(
                target_company_data, competitor_companies
            )

            if comparison_df.empty:
                print("No comparison data available")
                return None

            # Generate insights
            print("Generating competitive insights...")
            insights = competitive_analyzer.generate_comparison_insights(
                target_company_data, comparison_df
            )

            # Get sector benchmarks
            benchmarks = competitive_analyzer.get_sector_benchmarks(
                comparison_df, " > ".join(sector_hierarchy)
            )

            # Generate visualizations
            print("Creating visualizations...")
            chart_paths = self._generate_all_charts(
                comparison_df, target_company_data, competitor_companies, output_dir
            )

            # Generate AI-powered competitive summary
            print("Generating AI competitive summary...")
            competitive_summary = gemini_service.generate_competitive_summary(
                target_company_data, competitor_companies, insights, benchmarks
            )

            # Add summary to insights
            if competitive_summary:
                insights["ai_summary"] = competitive_summary
                print("✅ AI competitive summary generated")
            else:
                print("⚠️ AI competitive summary generation failed")

            # Create PDF report
            print("Generating PDF report...")
            company_name = target_company_data.get("company_overview", {}).get(
                "name", "target_company"
            )
            safe_company_name = company_name.replace(" ", "_").replace("/", "_").lower()
            pdf_path = os.path.join(
                output_dir, f"{safe_company_name}_benchmark_report.pdf"
            )

            if pdf_report_generator.create_benchmark_report(
                target_company_data, insights, chart_paths, pdf_path
            ):
                print(f"Benchmark analysis complete. Report saved to: {pdf_path}")
                return pdf_path  # Return the PDF path instead of True
            else:
                print("Failed to create PDF report")
                return None  # Return None instead of False

        except Exception as e:
            print(f"Error in benchmarking flow: {e}")
            return None  # Return None instead of False

    def _generate_all_charts(
        self, comparison_df, target_data, competitor_data, output_dir
    ):
        """Generate all visualization charts."""
        chart_paths = {}
        target_company_name = target_data.get("company_overview", {}).get(
            "name", "Target Company"
        )

        print(f"Generating charts for {len(comparison_df)} companies...")

        # Radar chart
        radar_path = os.path.join(output_dir, "radar_chart.png")
        try:
            if chart_generator.create_radar_chart(
                comparison_df, target_company_name, radar_path
            ):
                chart_paths["radar_chart"] = radar_path
                print("✅ Radar chart created")
            else:
                print("⚠️ Radar chart skipped")
        except Exception as e:
            print(f"❌ Error creating radar chart: {e}")

        # Heatmap
        heatmap_path = os.path.join(output_dir, "performance_heatmap.png")
        try:
            if chart_generator.create_heatmap(comparison_df, heatmap_path):
                chart_paths["performance_heatmap"] = heatmap_path
                print("✅ Heatmap created")
            else:
                print("⚠️ Heatmap skipped")
        except Exception as e:
            print(f"❌ Error creating heatmap: {e}")

        # Bubble chart
        bubble_path = os.path.join(output_dir, "bubble_chart.png")
        try:
            if chart_generator.create_bubble_chart(
                comparison_df, target_company_name, bubble_path
            ):
                chart_paths["bubble_chart"] = bubble_path
                print("✅ Bubble chart created")
            else:
                print("⚠️ Bubble chart skipped")
        except Exception as e:
            print(f"❌ Error creating bubble chart: {e}")

        # Quadrant analysis
        quadrant_path = os.path.join(output_dir, "quadrant_analysis.png")
        try:
            if chart_generator.create_quadrant_analysis(
                comparison_df, target_company_name, quadrant_path
            ):
                chart_paths["quadrant_analysis"] = quadrant_path
                print("✅ Quadrant analysis created")
            else:
                print("⚠️ Quadrant analysis skipped")
        except Exception as e:
            print(f"❌ Error creating quadrant analysis: {e}")

        # Distribution plots
        distribution_path = os.path.join(output_dir, "distribution_plots.png")
        try:
            if chart_generator.create_distribution_plots(
                comparison_df, target_company_name, distribution_path
            ):
                chart_paths["distribution_plots"] = distribution_path
                print("✅ Distribution plots created")
            else:
                print("⚠️ Distribution plots skipped")
        except Exception as e:
            print(f"❌ Error creating distribution plots: {e}")

        # Scorecard
        scorecard_path = os.path.join(output_dir, "performance_scorecard.png")
        try:
            benchmarks = competitive_analyzer.get_sector_benchmarks(
                comparison_df,
                target_data.get("company_overview", {}).get("sector_hierarchy", [""])[
                    -1
                ],
            )
            if comparison_visualizer.create_scorecard(
                target_data, benchmarks, scorecard_path
            ):
                chart_paths["performance_scorecard"] = scorecard_path
                print("✅ Scorecard created")
            else:
                print("⚠️ Scorecard skipped")
        except Exception as e:
            print(f"❌ Error creating scorecard: {e}")

        # Fundraise analysis
        fundraise_path = os.path.join(output_dir, "fundraise_analysis.png")
        try:
            if comparison_visualizer.create_fundraise_analysis(
                target_data, competitor_data, fundraise_path
            ):
                chart_paths["fundraise_analysis"] = fundraise_path
                print("✅ Fundraise analysis created")
            else:
                print("⚠️ Fundraise analysis skipped")
        except Exception as e:
            print(f"❌ Error creating fundraise analysis: {e}")

        # Traction comparison
        traction_path = os.path.join(output_dir, "traction_comparison.png")
        try:
            if comparison_visualizer.create_traction_comparison(
                target_data, competitor_data, traction_path
            ):
                chart_paths["traction_comparison"] = traction_path
                print("✅ Traction comparison created")
            else:
                print("⚠️ Traction comparison skipped")
        except Exception as e:
            print(f"❌ Error creating traction comparison: {e}")

        return chart_paths


# Global instances
pdf_processing_flow = PDFProcessingFlow()
benchmarking_flow = BenchmarkingFlow()

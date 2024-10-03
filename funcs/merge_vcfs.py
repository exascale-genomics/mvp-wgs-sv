import os
import subprocess
import sys
import argparse
import glob

# python3 ./merge_vcfs.py --input /lus/grand/projects/GeomicVar/rodriguez/1kg_proj/output/ --output /lus/grand/projects/GeomicVar/rodriguez/1kg_proj/output//merged/

def count_vcf_files(main_vcf_dir):
    """Count the number of VCF files in the specified directory and its subdirectories."""
    return len(glob.glob(os.path.join(main_vcf_dir, '**', '*.vcf'), recursive=True))

def generate_pbs_script(main_vcf_dir, output_dir, pbs_script_path, test=False):
    # Count the number of VCF files
    num_vcf_files = count_vcf_files(main_vcf_dir)

    # Determine the number of nodes based on the number of VCF files
    nodes = 1 if test else (num_vcf_files // 2 + (num_vcf_files % 2 > 0))  # 1 node for test, otherwise 2 per VCF file

    # Set PBS parameters based on test mode
    queue = "debug" if test else "preemptable"
    walltime = "01:00:00" if test else "06:00:00"  # 1 hour for test, 6 hours for normal
    ncpus = 64  # Always set to 64

    # Write the PBS script content to the specified path
    with open(pbs_script_path, 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("#PBS -N VCF_Processing\n")
        f.write("#PBS -l select={}\n".format(nodes))
        f.write("#PBS -l walltime={}\n".format(walltime))
        f.write("#PBS -o {}/output.log\n".format(output_dir))
        f.write("#PBS -e {}/error.log\n".format(output_dir))
        f.write("#PBS -j oe\n")
        f.write("#PBS -A GeomicVar\n")  # Project account
        f.write("#PBS -l filesystems=home:grand\n")  # Specify required filesystems
        f.write("#PBS -q {}\n".format(queue))  # Specify the queue

        # Define and export the BCFTOOLS variable
        f.write("BCFTOOLS=\"/grand/projects/GeomicVar/rodriguez/1kg_proj/data/tools/bcftools/bcftools-1.21/bcftools\"\n")
        f.write("export BCFTOOLS\n")  # Export the variable

        f.write("# Find all VCF files in the main directory and its subdirectories\n")
        f.write("vcf_files=($(find \"{}\" -type f -name \"*.vcf\"))\n\n".format(main_vcf_dir))

        f.write("# If in test mode, limit to the first 2 VCF files\n")
        f.write("if [ \"{}\" == \"true\" ]; then\n".format(str(test).lower()))  # Corrected line
        f.write("    vcf_files=(${vcf_files[@]:0:2})\n")  # Limit to 2 files in test mode
        f.write("fi\n\n")  # Close the if statement

        # Function to convert and index a VCF file
        f.write("# Function to convert and index a VCF file\n")
        f.write("convert_and_index() {\n")
        f.write("    local vcf=\"$1\"\n")
        f.write("    echo \"Converting $vcf to $vcf.gz using bcftools\"\n")
        f.write("    start_time=$(date +%s)  # Start time for conversion\n")
        f.write("    output_gz=\"{}/$(basename \"${vcf%.vcf}.vcf.gz\")\"\n".format(output_dir))
        f.write("    \"$BCFTOOLS\" view -Oz -o \"$output_gz\" \"$vcf\"\n")
        f.write("    end_time=$(date +%s)  # End time for conversion\n")
        f.write("    echo \"Time taken to convert $vcf: $((end_time - start_time)) seconds\"\n\n")

        # Add the reheadering step
        f.write("    # Create a temporary file for new sample names\n")
        f.write("    sample_name=\"$(basename \"$vcf\" .final_final.vcf)\"\n")
        f.write("    sample_name_file=\"/lus/grand/projects/GeomicVar/rodriguez/1kg_proj/output/merged/$sample_name.sample_name.txt\"\n")
        f.write("    echo $sample_name > \"$sample_name_file\"\n")
        f.write("    reheadered_vcf=\"/lus/grand/projects/GeomicVar/rodriguez/1kg_proj/output/merged/$(basename \"${vcf%.vcf}_reheadered.vcf.gz\")\"\n")
        f.write("    echo \"Updating sample name in $output_gz\"\n")
        f.write("    \"$BCFTOOLS\" reheader -s \"$sample_name_file\" -o \"$reheadered_vcf\" \"$output_gz\"\n")

        # Index the reheadered VCF file
        f.write("    echo \"Indexing $reheadered_vcf using bcftools\"\n")
        f.write("    \"$BCFTOOLS\" index \"$reheadered_vcf\"\n")
        f.write("    end_time=$(date +%s)  # End time for indexing\n")
        f.write("    echo \"Time taken to index $reheadered_vcf: $((end_time - start_time)) seconds\"\n")
        f.write("}\n\n")  # Closing brace for the function

        f.write("export -f convert_and_index  # Export the function for parallel execution\n\n")

        # Run the conversion and indexing in parallel using mpiexec with heredoc
        f.write("for vcf in \"${vcf_files[@]}\"; do\n")  # Changed line
        f.write("    convert_and_index \"$vcf\" &\n")
        f.write("done\n")
        f.write("wait\n\n")  # Changed line

        # Define the output directory where the merged VCF files will be stored
        merged_directory = output_dir  # Adjust this if your merged directory is different

        # Find all .vcf.gz files in the merged directory
        vcf_files = glob.glob(os.path.join(merged_directory, '*reheadered.vcf.gz'))

        # Write the merging command using the found VCF files
        f.write("# Find all reheadered updated VCF files in the merged output directory and its subdirectories\n")
        f.write("vcf_reheadered_files=($(find \"{}\" -type f -name \"*reheadered.vcf.gz\"))\n\n".format(output_dir))
        # Write the merging command using the found VCF files
        f.write("# Merge VCF.GZ files using bcftools\n")
        output_file = os.path.join(merged_directory, "merged.vcf.gz")
        f.write("echo \"output_file=\"{}\"\n".format(output_file))
        f.write("echo \"Merging VCF.GZ files into $output_file\"\n")
        f.write("start_time=$(date +%s)  # Start time for merging\n")
        f.write("\"$BCFTOOLS\" merge -o \"$output_file\" -O z \"${vcf_reheadered_files[@]}\"\n")  # Use the new VCF files
        f.write("end_time=$(date +%s)  # End time for merging\n")
        f.write("echo \"Time taken to merge VCF.GZ files: $((end_time - start_time)) seconds\"\n\n")

        # Index the merged VCF.GZ file using Tabix
        f.write("echo \"Creating Tabix index for $output_file\"\n")
        f.write("start_time=$(date +%s)  # Start time for indexing merged file\n")
        f.write("\"$BCFTOOLS\" index \"$output_file\"\n")
        f.write("end_time=$(date +%s)  # End time for indexing merged file\n")
        f.write("echo \"Time taken to index $output_file: $((end_time - start_time)) seconds\"\n")

    # Make the PBS script executable
    os.chmod(pbs_script_path, 0o755)

    print(f"PBS script generated at: {pbs_script_path}")

def submit_pbs_script(pbs_script_path):
    # Submit the PBS script using qsub
    try:
        subprocess.run(['qsub', pbs_script_path], check=True)
        print(f"PBS script submitted: {pbs_script_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error submitting PBS script: {e}")
        sys.exit(1)

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Generate and submit a PBS script for VCF processing.')
    parser.add_argument('-i', '--input', required=True, help='Input VCF directory')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    parser.add_argument('--test', action='store_true', help='Test mode: process only 2 VCF files')

    args = parser.parse_args()

    main_vcf_directory = args.input
    output_directory = args.output
    pbs_script_file = os.path.join(output_directory, "vcf_processing.pbs")

    # Generate the PBS script
    generate_pbs_script(main_vcf_directory, output_directory, pbs_script_file, args.test)

    # Submit the PBS script
    #submit_pbs_script(pbs_script_file)

if __name__ == "__main__":
    main()

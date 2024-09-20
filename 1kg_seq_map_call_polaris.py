import os
import glob
import argparse
import subprocess
import math
import time
import uuid

def find_cram_files(cram_dir):
    """
    Find .cram files with corresponding .crai files in the given directory.
    """
    cram_files = []
    for root, dirs, files in os.walk(cram_dir):
        for file in files:
            if file.endswith('.cram'):
                cram_path = os.path.join(root, file)
                crai_path = cram_path + '.crai'
                if os.path.exists(crai_path):
                    cram_files.append(cram_path)
    return cram_files

def is_sample_completed(sample_output_dir, sample_name):
    """
    Check if a sample has completed processing by looking for final output files.
    """
    final_bam = os.path.join(sample_output_dir, f"{sample_name}_final.bam")
    final_vcf = os.path.join(sample_output_dir, f"{sample_name}_final.vcf")
    return os.path.exists(final_bam) and os.path.exists(final_vcf)

def create_job_script(job_name, container_path, output_dir, account, cram_files, num_gpus, cpu_only, test_mode, test_samples, test_nodes, use_valgrind):
    job_script = os.path.join(output_dir, f"{job_name}.sh")
    with open(job_script, 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("#PBS -N {}\n".format(job_name))
        if test_mode:
            actual_nodes = min(test_nodes, len(cram_files))  # Use at most as many nodes as samples
            if cpu_only:
                f.write("#PBS -l select={}:ncpus=64\n".format(actual_nodes))  # Test mode with CPU-only
            else:
                f.write("#PBS -l select={}:ncpus=32:ngpus={}\n".format(actual_nodes, num_gpus))  # Test mode with GPUs
            f.write("#PBS -l walltime=04:00:00\n")  # 4 hours for test mode
        else:
            if cpu_only:
                f.write("#PBS -l select=10:ncpus=64\n")  # Adjust ncpus based on your CPU-only node configuration
            else:
                f.write(f"#PBS -l select=10:ncpus=32:ngpus={num_gpus}\n")
            f.write("#PBS -l walltime=03:00:00\n")  # 3 hours for prod mode with 10 or fewer nodes
        f.write(f"#PBS -A {account}\n")  # Specify the project account
        f.write("#PBS -l filesystems=home:grand\n")  # Specify required filesystems
        f.write("#PBS -q {}\n".format("preemptable" if test_mode else "prod"))  # Specify queue
        f.write("#PBS -r y\n")  # Make the job rerunnable
        f.write("\n")
        f.write("module use /soft/spack/gcc/0.6.1/install/modulefiles/Core\n")
        f.write("module load singularityce\n")
        f.write("module load craype-accel-nvidia90\n")  # Load the new module
        if use_valgrind:
            f.write("module load valgrind4hpc\n")  # Load Valgrind module
        f.write("\n")
        f.write(f"export CONTAINER_PATH={container_path}\n")
        f.write(f"export OUTPUT_DIR={output_dir}\n")
        f.write("\n")

        # Calculate the number of nodes, ranks, and GPUs/CPUs
        f.write("NNODES=$(wc -l < $PBS_NODEFILE)\n")
        if cpu_only:
            f.write("NCPUS_PER_NODE=64\n")  # Adjust this based on your CPU-only node configuration
        else:
            f.write(f"NGPUS_PER_NODE={num_gpus}\n")
        f.write("NRANKS_PER_NODE=1\n")  # Set NRANKS_PER_NODE to 1
        f.write("NTHREADS=64\n")
        f.write("NDEPTH=64\n")
        f.write("NTOTRANKS=$NNODES\n")  # Total ranks is now equal to the number of nodes
        f.write("\n")
        if not cpu_only:
            f.write("export NGPUS_PER_NODE\n")
        f.write("\n")

        # Save the current environment and function definitions to a file
        f.write("cat << 'EOF' > $PBS_O_WORKDIR/job_env.sh\n")
        f.write("#!/bin/bash\n")
        f.write("export CONTAINER_PATH=" + container_path + "\n")
        f.write("export OUTPUT_DIR=" + output_dir + "\n")
        if not cpu_only:
            f.write("export NGPUS_PER_NODE=$NGPUS_PER_NODE\n")
        f.write("\n")
        f.write("process_cram() {\n")
        f.write("    cram_file=\"$1\"\n")
        f.write("    gpu_device=\"$2\"\n")
        f.write("    echo \"Debug: Processing CRAM file: $cram_file\"\n")
        f.write("    echo \"Debug: Using GPU device: $gpu_device\"\n")
        f.write("    echo \"Debug: cram_file=$cram_file\"\n")
        f.write("    echo \"Debug: gpu_device=$gpu_device\"\n")
        f.write("    echo \"Debug: CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES\"\n")
        f.write("    sample_name=$(basename \"$cram_file\" | sed 's/\.cram$//')\n")
        f.write("    echo \"Debug: sample_name=$sample_name\"\n")
        f.write("    cram_dir=$(dirname \"$cram_file\")\n")
        f.write("    echo \"Debug: cram_dir=$cram_dir\"\n")
        f.write("    sample_output_dir=\"${OUTPUT_DIR}/${sample_name}.final\"\n")
        f.write("    echo \"Debug: sample_output_dir=$sample_output_dir\"\n")
        f.write("    mkdir -p \"$sample_output_dir\"\n")
        f.write("\n")
        f.write("    echo \"Processing CRAM file: $cram_file\"\n")
        f.write("    echo \"Sample name: $sample_name\"\n")
        f.write("    echo \"Output directory: $sample_output_dir\"\n")
        f.write("\n")
        
        # Create a unique temporary directory for each sample
        f.write("    tmpdir=\"$PBS_O_WORKDIR/tmp_$sample_name\"\n")
        f.write("    mkdir -p \"$tmpdir\"\n")
        f.write("    echo \"Using temporary directory: $tmpdir\"\n")
        
        # Set the Singularity temporary directory
        f.write("    export SINGULARITY_TMPDIR=\"$tmpdir\"\n")
        
        # Check GPU availability
        f.write("    if command -v nvidia-smi &> /dev/null; then\n")
        f.write("        echo \"GPU information before processing:\" >> \"$tmpdir/gpu_usage.txt\"\n")
        f.write("        nvidia-smi >> \"$tmpdir/gpu_usage.txt\"\n")
        f.write("    else\n")
        f.write("        echo \"nvidia-smi not available, cannot check GPU usage\" >> \"$tmpdir/gpu_usage.txt\"\n")
        f.write("    fi\n")
        f.write("\n")
        
        # Command 1: bam2fq with GPU support and optional Valgrind
        f.write("    echo \"Running bam2fq with GPU support")
        if use_valgrind:
            f.write(" and Valgrind")
        f.write("\"\n")
        if use_valgrind:
            f.write("    valgrind --tool=callgrind --callgrind-out-file=\"$sample_output_dir/bam2fq_callgrind.out\" \\\n")
        f.write("    singularity exec \\\n")
        f.write("        -H /grand/projects/GeomicVar/rodriguez \\\n")
        f.write("        -W /grand/projects/GeomicVar/rodriguez/1kg_proj/tmp \\\n")
        f.write("        --bind /grand/projects/GeomicVar/rodriguez:/grand/projects/GeomicVar/rodriguez \\\n")
        f.write("        --bind \"$cram_dir\":\"$cram_dir\" \\\n")
        f.write("        --bind \"$OUTPUT_DIR\":\"$OUTPUT_DIR\" \\\n")
        if not cpu_only:
            f.write("        --nv \"$CONTAINER_PATH\" \\\n")
        else:
            f.write("        :\"$CONTAINER_PATH\" \\\n")
        f.write("        pbrun bam2fq \\\n")
        f.write("        --in-bam \"$cram_file\" \\\n")
        f.write("        --out-prefix \"$sample_output_dir/output\" \\\n")
        f.write("        --num-threads 20 \\\n")  # Set num-threads to 20
        f.write("        --ref /grand/projects/GeomicVar/rodriguez/1kg_proj/data/reference/GRCh38_CRAM/GRCh38_full_analysis_set_plus_decoy_hla.fa \\\n")
        if use_valgrind:
            f.write("        2> \"$sample_output_dir/bam2fq_valgrind.log\"\n")
        else:
            f.write("        2> \"$sample_output_dir/bam2fq.log\"\n")
        f.write("\n")
        
        # Check GPU usage after bam2fq
        f.write("    if command -v nvidia-smi &> /dev/null; then\n")
        f.write("        echo \"GPU information after bam2fq:\" >> \"$tmpdir/gpu_usage.txt\"\n")
        f.write("        nvidia-smi >> \"$tmpdir/gpu_usage.txt\"\n")
        f.write("    fi\n")
        f.write("\n")
        
        # Add a 10-second sleep between commands
        f.write("    echo \"Sleeping for 10 seconds between commands\"\n")
        f.write("    sleep 10\n")
        f.write("\n")

        # Command 2: deepvariant_germline with GPU support and optional Valgrind
        f.write("    echo \"Running deepvariant_germline with GPU support")
        if use_valgrind:
            f.write(" and Valgrind")
        f.write("\"\n")
        if use_valgrind:
            f.write("    valgrind --tool=callgrind --callgrind-out-file=$sample_output_dir/deepvariant_callgrind.out \\\n")
        if not cpu_only:
            gpu_list = ",".join(str(i) for i in range(num_gpus))
            f.write(f"    CUDA_VISIBLE_DEVICES={gpu_list} singularity exec \\\n")
        else:
            f.write("    singularity exec \\\n")
        f.write("        -H /grand/projects/GeomicVar/rodriguez \\\n")
        f.write("        -W /grand/projects/GeomicVar/rodriguez/1kg_proj/tmp \\\n")
        f.write("        --bind /grand/projects/GeomicVar/rodriguez:/grand/projects/GeomicVar/rodriguez \\\n")
        f.write("        --bind $cram_dir:$cram_dir \\\n")
        f.write("        --bind $OUTPUT_DIR:$OUTPUT_DIR \\\n")
        if not cpu_only:
            f.write("        --nv $CONTAINER_PATH \\\n")
        else:
            f.write("        $CONTAINER_PATH \\\n")
        f.write("        pbrun deepvariant_germline \\\n")
        f.write("        --ref /grand/projects/GeomicVar/rodriguez/1kg_proj/data/reference/GRCh38_CRAM/GRCh38_full_analysis_set_plus_decoy_hla.fa \\\n")
        f.write("        --in-fq $sample_output_dir/output_1.fastq.gz $sample_output_dir/output_2.fastq.gz \\\n")
        f.write("        --out-bam $sample_output_dir/${sample_name}_final.bam \\\n")
        f.write("        --out-variants $sample_output_dir/${sample_name}_final.vcf \\\n")
        if use_valgrind:
            f.write("        2> $sample_output_dir/deepvariant_valgrind.log\n")
        else:
            f.write("        2> $sample_output_dir/deepvariant.log\n")
        f.write("\n")
        
        # Add post-deepvariant GPU debugging information
        f.write("    echo \"Debug: CUDA_VISIBLE_DEVICES after deepvariant: $CUDA_VISIBLE_DEVICES\"\n")
        f.write("    echo \"Debug: GPU usage after deepvariant:\"\n")
        f.write("    nvidia-smi\n")
        f.write("\n")
        
        # Check GPU usage after deepvariant_germline
        f.write("    if command -v nvidia-smi &> /dev/null; then\n")
        f.write("        echo \"GPU information after deepvariant_germline:\" >> \"$tmpdir/gpu_usage.txt\"\n")
        f.write("        nvidia-smi >> \"$tmpdir/gpu_usage.txt\"\n")
        f.write("    fi\n")
        f.write("}\n")
        f.write("\n")
        f.write("distribute_samples() {\n")
        f.write("    local node_index=$1\n")
        f.write("    local total_nodes=$2\n")
        f.write("    local samples_file=$3\n")
        f.write("    if [ ! -f \"$samples_file\" ]; then\n")
        f.write("        echo \"Error: samples file '$samples_file' not found\"\n")
        f.write("        return 1\n")
        f.write("    fi\n")
        f.write("    local sample_count=$(wc -l < \"$samples_file\")\n")
        f.write("    if [ \"$total_nodes\" -eq 0 ]; then\n")
        f.write("        echo \"Error: total_nodes is 0\"\n")
        f.write("        return 1\n")
        f.write("    fi\n")
        f.write("    local samples_per_node=$(( (sample_count + total_nodes - 1) / total_nodes ))\n")
        f.write("    local start_index=$(( node_index * samples_per_node ))\n")
        f.write("    local end_index=$(( start_index + samples_per_node - 1 ))\n")
        f.write("    if [ $end_index -ge $sample_count ]; then\n")
        f.write("        end_index=$((sample_count - 1))\n")
        f.write("    fi\n")
        
        # Use sed to filter out lines that are not valid sample files
        f.write("    sed -n \"$((start_index + 1)),$((end_index + 1))p\" \"$samples_file\" | while read -r sample; do\n")
        f.write("        if [[ -n \"$sample\" && -f \"$sample\" ]]; then\n")  # Check if the line is not empty and is a file
        f.write("            echo \"$sample\"\n")  # Output the sample for further processing
        f.write("        fi\n")
        f.write("    done\n")
        f.write("}\n")
        f.write("\n")
        f.write("process_node_samples() {\n")
        f.write("    local rank=$1\n")
        f.write("    local nnodes=$2\n")
        f.write("    echo \"Debug: process_node_samples called with rank=$rank, nnodes=$nnodes\"\n")
        f.write("    local node_samples=$(distribute_samples $rank $nnodes $PBS_O_WORKDIR/cram_files.txt)\n")
        f.write("    echo \"Debug: Node $rank processing samples:\"\n")
        f.write("    echo \"$node_samples\"\n")
        f.write("    echo \"$node_samples\" | while read cram_file; do\n")
        f.write("        if [ ! -z \"$cram_file\" ]; then\n")
        f.write("            process_cram \"$cram_file\" \"$CUDA_VISIBLE_DEVICES\"\n")
        f.write("        fi\n")
        f.write("    done\n")
        f.write("}\n")
        f.write("export -f process_cram distribute_samples process_node_samples\n")
        f.write("EOF\n")
        f.write("\n")

        # Write CRAM files to a temporary file
        f.write("cat << EOF > $PBS_O_WORKDIR/cram_files.txt\n")
        for cram_file in cram_files:
            f.write(f"{cram_file}\n")
        f.write("EOF\n")
        f.write("\n")
        f.write("echo \"Debug: Contents of cram_files.txt:\"\n")
        f.write("cat $PBS_O_WORKDIR/cram_files.txt\n")
        f.write("\n")

        # Calculate the number of samples and nodes
        f.write("NSAMPLES=$(wc -l < $PBS_O_WORKDIR/cram_files.txt)\n")
        f.write("NNODES=$(wc -l < $PBS_NODEFILE)\n")
        f.write("echo \"Debug: Number of samples: $NSAMPLES\"\n")
        f.write("echo \"Debug: Number of nodes: $NNODES\"\n")
        f.write("\n")

        # Debugging output for environment variables
        f.write("env > $PBS_O_WORKDIR/env_variables.txt\n")
        f.write("echo \"Debug: Running mpiexec with NNODES=$NNODES\"\n")
        f.write("mpiexec -n $NNODES -ppn 1 --depth=${NDEPTH} --cpu-bind depth --env OMP_NUM_THREADS=${NTHREADS} --env OMP_PLACES=threads bash -c \"source $PBS_O_WORKDIR/job_env.sh && process_node_samples \$PMI_RANK $NNODES\"\n")

    return job_script

def main(cram_dir, output_dir, container_path, account, num_gpus, cpu_only, test_mode=False, test_samples=1, test_nodes=1, use_valgrind=False):
    # Convert to absolute paths
    cram_dir = os.path.abspath(cram_dir)
    output_dir = os.path.abspath(output_dir)
    container_path = os.path.abspath(container_path)

    # Find .cram files with corresponding .crai files
    cram_files = find_cram_files(cram_dir)
    print(f"Debug: Found {len(cram_files)} total CRAM files")

    if not cram_files:
        print("No CRAM files with corresponding CRAI files found. Exiting.")
        return

    # Filter out completed samples and select the required number for testing
    incomplete_cram_files = []
    for cram_file in cram_files:
        sample_name = os.path.basename(cram_file).replace('.cram', '')
        sample_output_dir = os.path.join(output_dir, f"{sample_name}.final")
        if not is_sample_completed(sample_output_dir, sample_name):
            incomplete_cram_files.append(cram_file)
            print(f"Debug: Added incomplete sample: {cram_file}")
            if test_mode and len(incomplete_cram_files) == test_samples:
                break

    if not incomplete_cram_files:
        print("All samples have been processed. No job submitted.")
        return

    if test_mode:
        if len(incomplete_cram_files) < test_samples:
            print(f"Warning: Only {len(incomplete_cram_files)} incomplete sample(s) found. Processing all of them.")
        else:
            incomplete_cram_files = incomplete_cram_files[:test_samples]
        print(f"Test mode: Processing {len(incomplete_cram_files)} sample(s) on {test_nodes} node(s).")
    else:
        print(f"Found {len(incomplete_cram_files)} incomplete CRAM files to process.")

    print("Debug: Samples to be processed:")
    for cram_file in incomplete_cram_files:
        print(f"  {cram_file}")

    # Submit jobs
    job_name = "cram_processing"
    try:
        job_script = create_job_script(job_name, container_path, output_dir, account, incomplete_cram_files, 
                                       num_gpus, cpu_only, test_mode, test_samples, test_nodes, use_valgrind)
    except Exception as e:
        print(f"Error creating job script: {e}")
        return

    # Check if mpiexec command is available
    if not subprocess.run(['which', 'mpiexec'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
        print("Error: 'mpiexec' command not found. Make sure you're on a system with MPI installed.")
        return

    # Submit job
    command = f"qsub {job_script}"
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
        print(f"Job '{job_name}' submitted successfully for {len(incomplete_cram_files)} incomplete sample(s).")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error submitting job '{job_name}':")
        print(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
    except Exception as e:
        print(f"Unexpected error submitting job '{job_name}':")
        print(str(e))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Submit CRAM processing jobs to a cluster using qsub.")
    parser.add_argument("--cram_dir", required=True, help="Directory containing sample subdirectories with .cram files")
    parser.add_argument("--output_dir", required=True, help="Directory where output files will be saved")
    parser.add_argument("--container_path", required=True, help="Path to the Singularity container file (.sif)")
    parser.add_argument("--account", required=True, help="Account name for job submission")
    parser.add_argument("--num_gpus", type=int, default=4, help="Number of GPUs to use per node")
    parser.add_argument("--cpu_only", action="store_true", help="Run in CPU-only mode without using GPUs")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    parser.add_argument("--test_samples", type=int, default=1, help="Number of samples to process in test mode")
    parser.add_argument("--test_nodes", type=int, default=1, help="Number of nodes to use in test mode")
    parser.add_argument("--use_valgrind", action="store_true", help="Use Valgrind for profiling")
    args = parser.parse_args()

    main(args.cram_dir, args.output_dir, args.container_path, args.account, args.num_gpus, args.cpu_only, 
         test_mode=args.test, test_samples=args.test_samples, test_nodes=args.test_nodes, use_valgrind=args.use_valgrind)

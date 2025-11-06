document.getElementById("run-btn").addEventListener("click", () => {
  const output = document.getElementById("output");
  output.textContent = "Starting AWS Provisioning Simulation...\n\n";

  const log = [
    "🖥️  Launching EC2 instance 'WebServer01' in region us-east-1 with AMI ami-0abcd1234",
    "🪣 Creating S3 bucket 'dre-backup-bucket' in region us-east-1 with encryption=AES256",
    "🔐 Creating IAM role 'AppAccessRole' with policy AmazonS3FullAccess",
    "✅ Provisioning complete!"
  ];

  log.forEach((line, i) => {
    setTimeout(() => output.textContent += line + "\n", 800 * i);
  });
});

resource "random_password" "tunnel_secret" {
  length  = 64
  special = false
}

# Terraform의 Cloudflare 프로바이더가 업데이트되면서 
# 기존 cloudflare_tunnel 리소스가 **cloudflare_zero_trust_tunnel_cloudflared**로 이름이 변경
# 리소스 타입을 "cloudflare_tunnel" > "cloudflare_zero_trust_tunnel_cloudflared" 로 변경
resource "cloudflare_tunnel" "vmware_tunnel" {
  account_id = var.cloudflare_account_id
  name       = "vmware-local-tunnel"
  secret     = base64encode(random_password.tunnel_secret.result)
}

# https://junhanshin.com 으로 접속 했을 때
resource "cloudflare_record" "vmware_dns" {
  zone_id = var.cloudflare_zone_id
  name    = "@"
  content = "${cloudflare_tunnel.vmware_tunnel.id}.cfargotunnel.com"
  type    = "CNAME"
  proxied = true
}

# # https://dev.junhanshin.com 으로 접속 했을 때
# resource "cloudflare_record" "vmware_dns2" {
#   zone_id = var.cloudflare_zone_id
#   name    = "dev"  # << 이곳의 이름을 바꿔 원하는 만큼 서브 도메인 추가 가능
#   content = "${cloudflare_tunnel.vmware_tunnel.id}.cfargotunnel.com"
#   type    = "CNAME"
#   proxied = true
# }

resource "cloudflare_tunnel_config" "vmware_config" {
  account_id = cloudflare_tunnel.vmware_tunnel.account_id
  tunnel_id  = cloudflare_tunnel.vmware_tunnel.id

  config {
    # dev.junhanshin.com 관련 ingress_rule
    # ingress_rule {
    #   hostname = "dev.${var.domain_name}"
    #   # ALB의 DNS나 Master EC2의 localhost 등으로 트래픽 전달
    #   service  = "http://dev.junhanshin.com:80" 
    # }

    ingress_rule {
      hostname = var.domain_name
      # ALB의 DNS나 Master EC2의 localhost 등으로 트래픽 전달
      service  = "http://localhost:80" 
    }

    ingress_rule {
      service = "http_status:404"
    }
  }
}
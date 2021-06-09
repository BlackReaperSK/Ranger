import discord
from requests import get, post
import json
import alive

token = 'Your DiscordBot Token!'

client = discord.Client()
@client.event
async def on_ready():
    print("______________________________________")
    print("Bot Online")
    print(client.user.name)
    print(client.user.id)
    print("______________________________________")
    try:
      canal = client.get_channel(832336647164526643)
      await canal.send("**Sistema Online**")
      await client.change_presence(status=discord.Status.do_not_disturb,  activity=discord.Game('$help'))
    except:
      print("Error")
@client.event
async def on_message(message):
  msg = message.content
  if message.author == client.user:
    return
  #Comandos

  if message.content.startswith('$help'):
    embed=discord.Embed(title="Comandos", description="Comandos Disponives", color=0x000000)
    embed.set_thumbnail(url="https://pm1.narvii.com/6867/5f1ab99dca2dae517f456b58a69b6180caf2d540r1-437-336v2_hq.jpg")
    embed.add_field(name="$whatweb", value="Retorna oque o alvo Roda em Detalhes", inline=True)
    embed.add_field(name="$clear", value="Limpa o Chat", inline=True)
    embed.add_field(name="$help", value="Mostra a lista de comandos", inline=True)
    embed.add_field(name="$nmap", value="Usa o Scan do Nmap", inline=True)
    embed.add_field(name="$dnsdumsper", value="Check DNS do alvo", inline=True)
    embed.set_footer(text="By Blackreaper")
    await message.channel.send(embed=embed)

  #Clear

  if msg.startswith('$clear'):
    try:
      quantidade = msg.split('$clear ',1)[1]
      quantidade = int(quantidade)
    except:
      quantidade = 300
    deleted = await message.channel.purge(limit=quantidade)
    await message.channel.send('Chat Limpo')

  #Nmap

  if msg.startswith('$nmap'):
    hostname = msg.split('$nmap ', 1)[1]
    scan = get(f"https://api.hackertarget.com/nmap/?q={hostname}")
    resultado = scan.text
    if 'Error' in resultado:
      embed=discord.Embed(title="Nmap Scan", url="https://nmap.org/",description=f"Scan Report for {hostname}", color=0xd50101)
      embed.set_thumbnail(url="https://nmap.org/images/sitelogo.png")
      embed.add_field(name="Report Bellow", value="Erro, IP/Host não é valido.", inline=False)
      embed.set_footer(text="By Blackreaper")
    else:
      embed=discord.Embed(title="Nmap Scan", url="https://nmap.org/", description=f"Scan Report for {hostname}", color=0xd50101)
      embed.set_thumbnail(url="https://nmap.org/images/sitelogo.png")
      embed.add_field(name="Report Bellow", value=f"{resultado}", inline=False)
      embed.set_footer(text="By Blackreaper")
    await message.channel.send(embed=embed)

  #WhatWeb

  if msg.startswith('$whatweb'):
    hostname = msg.split('$whatweb ', 1)[1]
    whatweb = get(f'https://api.hackertarget.com/whatweb/?q={hostname}')
    resultado = whatweb.text
    if '301' in resultado:
      resultado = resultado.split("[0]\n\n\n\n", 1)[1]
    else:
      pass
    embed=discord.Embed(title="WhatWeb", url="https://tools.kali.org/web-applications/whatweb", description=f"Scan Report for {hostname}", color=0x0e0689)
    embed.set_thumbnail(url="https://357558-1266171-raikfcquaxqncofqfm.stackpathdns.com/wp-content/uploads/2017/10/whatweb-fingerprinter.jpg")
    embed=discord.Embed(title="WhatWeb", url="https://tools.kali.org/web-applications/whatweb", description=f"Scan Report for {hostname}", color=0x0e0689)
    embed.set_thumbnail(url="https://357558-1266171-raikfcquaxqncofqfm.stackpathdns.com/wp-content/uploads/2017/10/whatweb-fingerprinter.jpg")
    embed.add_field(name="Report Bellow", value=f"{resultado}", inline=False)
    embed.set_footer(text="By Blackreaper")
    await message.channel.send(embed=embed)

  #Dns Dumpster

  if msg.startswith('$dnsdumpster'):
    hostname = msg.split('$dnsdumpster ', 1)[1]
    dnsdumpster = get(f'https://api.hackertarget.com/hostsearch/?q={hostname}')
    resultado = dnsdumpster.text
    await message.channel.send("```css\n{X}DNS DUMPSTER SCAN:\n" + resultado + "```")

  #GeoIP

  if msg.startswith('$geoip'):
    hostname = msg.split('$geoip ', 1)[1]
    try:
      geoip = get(f'https://freegeoip.app/json/{hostname}')
      response = geoip.text
      response = json.loads(response)
      ip = response['ip'] ; pais = response['country_name'] ; estado = response['region_name']
      cidade = response['city'] ; zip_code = response['zip_code']; timezone = response['time_zone'];
      latitude = response['latitude'] ; longitude = response['longitude']
    except:
      ip = 'Error' 
    resultado = geoip.text
    if ip == 'Error':
      await message.channel.send("Erro: IP Invalido, Não encontrado ou Falha na API")
    else:
      await message.channel.send(f'```css\nIP: {ip}\nPais: {pais}\nEstado: {estado}\nCidade: {cidade}\nZipCode: {zip_code}\nLatitude/Longitude: {latitude}/{longitude}\n```')

  #SslAnalyze

  if msg.startswith('$testssl'):
    hostname = msg.split('$testssl ', 1)[1]
    sslyze = get(f'http://api.hackertarget.com/sslyze/?q={hostname}')
    resultado = sslyze.text
    url = 'https://pastebin.com/api/api_post.php'
    data = {
        'api_option' : 'paste',
        'api_dev_key' : '1PdFmWHB1XgaJ9B2kDZX943k0dLVcg6Z',
        'api_paste_code' : resultado,
        'api_paste_private' : '1',
        'api_paste_name' : 'Resultado $testssl ' + hostname,
        'api_paste_expire_date' : '10M',
        'api_paste_format' : 'php'
    }
    pastebin = post(url, data=data)
    await message.channel.send('Link:' + pastebin.text)

  #ShareDns

  if msg.startswith('$sharedns'):
    hostname = msg.split('$sharedns ', 1)[1]
    sharedns = get(f'https://api.hackertarget.com/findshareddns/?q={hostname}')
    resultado = sharedns.text
    await message.channel.send(resultado)    

  #Site Scan

  if msg.startswith('$scan'):
    hostname = msg.split('$scan ', 1)[1]
    if "https://" in hostname:
      pass
    elif "http://" in hostname:
      pass
    else:
      hostname = "http://" + hostname
    check =get(f"https://sitecheck.sucuri.net/api/v3/?scan={hostname}")
    bruto = json.loads(check.text)
    #TLS
    tls = bruto['tls']
    try:
      cert_issuer = tls['cert_issuer']
      cert_authority = tls['cert_authority']
    except:
      cert_authority = "Erro"
      cert_issuer = "Erro"
    #SITE
    site = bruto['site']
    ip = site['ip']
    try:
        powered_by = site['powered_by']
    except:
        powered_by = "Undefined/NotFound"
    try:
        running_on = site['running_on']
    except:
        running_on = "Nao Encontrado"
    try:
        redirects_to = site['redirects_to']
    except:
        redirects_to = "Não Redireciona"
    #rating TLS
    ratings = bruto['ratings']
    tls = ratings['tls']
    notatls = tls['passed']
    ratingtls = tls['rating']
    #security
    try:
        security = bruto['security']
        notaseg = security['passed']
        ratingseg = security['rating']
    except:
        notaseg = "Não Encontrado"
        ratingseg = "Não Encontrado"
    #software
    software = bruto['software']
    try:
        os = software['os']
        osname = os['name']
        osversion = os['version']
    except:
        osname = "Não encontrado"
        osversion = "Não encontrado"
    try:
        server = software['server']
        server = server[0]
        servername = server['name']
    except:
        servername = "Não Encontrado"
    try:
        serverversion = server['version']
    except:
        serverversion = "Não Encontrado"
    if 'cms' in check.text:
      cms = software['cms']
      cms = cms[0]
      cmsname = cms['name']
      cmsversion = cms['version']
      cmsbased = cms['based_on']
      safeversion = cms['safe_version']
      await message.channel.send(f"```css\nSite: {hostname}\nIPv4: {ip[0]}\nPoweredBy: {powered_by}\nAvaliação TLS/SSL: {notatls}\nNota TLS/SSL: {ratingtls}\nAvaliação Segurança: {notaseg}\nNota Segurança: {ratingseg}\nSistema Operacional: {osname}\nVersão do Sistema: {osversion}\nServidor: {servername}\nVersão do Servidor: {serverversion}\nCMS: {cmsname}\nVersão CMS: {cmsversion}\nCMS-Based: {cmsbased}\nVersão mais segura: {safeversion}```")
    else:
      await message.channel.send(f"```css\nSite: {hostname}\nIPv4: {ip[0]}\nPoweredBy: {powered_by}\nAvaliação TLS/SSL: {notatls}\nNota TLS/SSL: {ratingtls}\nAvaliação Segurança: {notaseg}\nNota Segurança: {ratingseg}\nSistema Operacional: {osname}\nVersão do Sistema: {osversion}\nServidor: {servername}\nVersão do Servidor: {serverversion}```")

alive.keep_alive()
client.run(token)

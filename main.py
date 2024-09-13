import asyncio
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

green_led = 20
blue_led =21
red_led = 16

GPIO.setup(green_led, GPIO.OUT)
GPIO.setup(blue_led, GPIO.OUT)
GPIO.setup(red_led, GPIO.OUT)

from asyncua import ua, uamethod, Server

async def main():

    server = Server()
    await server.init()

    server.set_endpoint("opc.tcp://10.4.1.145:4840")
    server.set_server_name("Example a24")

    server.set_security_policy(
        [
            ua.SecurityPolicyType.NoSecurity,
            ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
            ua.SecurityPolicyType.Basic256Sha256_Sign,
        ]
    )

    # setup our own namespace
    uri = "http://monURI"
    idx = await server.register_namespace(uri)

    async def func(parent_nodeid):
        parent = server.get_node(parent_nodeid)
        noeud_vert = await parent.get_child(["2:Vert"])
        await noeud_vert.write_value(False)

        noeud_blue = await parent.get_child(["2:Blue"])
        await noeud_blue.write_value(False)

        noeud_rouge = await parent.get_child(["2:Rouge"])
        await noeud_rouge.write_value(False)

    async def func_allume(parent_nodeid):
        parent = server.get_node(parent_nodeid)
        noeud_vert_allume = await parent.get_child(["2:Vert"])
        await noeud_vert_allume.write_value(True)

        noeud_blue_allume = await parent.get_child(["2:Blue"])
        await noeud_blue_allume.write_value(True)

        noeud_rouge_allume = await parent.get_child(["2:Rouge"])
        await noeud_rouge_allume.write_value(True)


    #Ajout du noeud
    LED1 = await server.nodes.objects.add_object(idx, "LED1")
    vert = await LED1.add_variable(idx, "Vert", False)
    await vert.set_writable()
    bleu = await LED1.add_variable(idx, "Blue", False)
    await bleu.set_writable()
    rouge = await LED1.add_variable(idx, "Rouge", False)
    await rouge.set_writable()
    methode = await LED1.add_method(idx, "methode", func)
    methode_lumiere_allume = await LED1.add_method(idx, "methode_lumiere_allume", func_allume)


    # starting!
    async with server:
        while True:
            await asyncio.sleep(0.1)
            if(await vert.read_value() == False):
                GPIO.output(green_led, GPIO.HIGH)
            else:
                GPIO.output(green_led, GPIO.LOW)
            if (await bleu.read_value() == False):
                GPIO.output(blue_led, GPIO.HIGH)
            else:
                GPIO.output(blue_led, GPIO.LOW)
            if (await rouge.read_value() == False):
                GPIO.output(red_led, GPIO.HIGH)
            else:
                GPIO.output(red_led, GPIO.LOW)




if __name__ == "__main__":
    asyncio.run(main())
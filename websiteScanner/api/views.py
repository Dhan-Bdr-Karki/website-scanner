from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import subprocess
import json
from whois import whois


class ScanWebsite(APIView):
    def post(self, request):
        url = request.data.get("url")
        if url:
            try:
                # Verifying domain registration
                domain_info = whois(url)
                print("success", domain_info)
                if domain_info.status != "available":
                    try:
                        output = subprocess.run(["/usr/bin/waybackurls", url], capture_output=True)
                        output_list = output.stdout.decode().strip().split("\n")
                        request.session["output"] = json.dumps(output_list)
                    except FileNotFoundError as e:
                        return Response({"status": "error", "message": "waybackurl command not found"})
                    return Response({"status": "success", "message": "Url " + url + " scanning is completed...", "output": output_list}, status=status.HTTP_200_OK)
                else:
                    return Response({"status": "error", "message": "Invalid domain"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"status": "error", "message": e}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"status": "error", "message": "No url provided"}, status=status.HTTP_400_BAD_REQUEST)


class DisplayQueryResult(APIView):
    def get(self, request):
        output = request.session.get("output")
        if output:
            return Response({"status": "success", "output": json.loads(output)}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "message": "No output to display"}, status=status.HTTP_404_NOT_FOUND)